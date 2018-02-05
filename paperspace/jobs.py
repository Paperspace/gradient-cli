import inspect
import json
import os
import sys
import tempfile
import time
import zipfile

import boto3
import botocore
import requests

from . import config
from .login import apikey
from .method import *

def zip_to_tmp(obj_name):
    zipname = os.path.join(tempfile.gettempdir(),
                           os.path.basename(obj_name)) + '.zip'
    outZipFile = zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED)

    if os.path.isdir(obj_name):
        for dirpath, dirnames, filenames in os.walk(obj_name):
            for filename in dirnames + filenames:
                filepath = os.path.join(dirpath, filename)
                basename = os.path.basename(filepath)
                if ('/.git/' not in filepath
                   and basename not in ['.git', '.gitignore']):
                    arcname = os.path.relpath(filepath, obj_name)
                    outZipFile.write(filepath, arcname)
    else:
        outZipFile.write(obj_name, os.path.basename(obj_name))

    outZipFile.close()
    return zipname


def print_json_pretty(res):
    print(json.dumps(res, indent=2, sort_keys=True))


def method(category, method, params):
    if 'apiKey' in params:
        config.PAPERSPACE_API_KEY = params['apiKey']
        del params['apiKey']
    elif not config.PAPERSPACE_API_KEY:
        config.PAPERSPACE_API_KEY = apikey()

    if method in ['artifactsGet', 'artifactsList', 'getJob', 'getJobs',
                  'getLogs']:

        http_method = 'GET'
        path = '/' + category + '/' + method

    elif method in ['artifactsDestroy', 'clone', 'destroy', 'stop']:

        http_method = 'POST'
        path = '/' + category + '/' + params['jobId'] + '/' + method
        del params['jobId']

    else:

        http_method = 'POST'
        path = '/' + category + '/' + method

    files = None
    if method == 'createJob' and 'workspace' in params:
        workspace = params['workspace']
        workspace_file = None
        if workspace and workspace != 'none':
            workspace_path = os.path.expanduser(workspace)
            if os.path.exists(workspace_path):
                if (not workspace_path.endswith('.zip')
                   and not workspace_path.endswith('.gz')):
                    workspace_file = zip_to_tmp(workspace_path)
                else:
                    workspace_file = workspace_path
            files = {'file': open(workspace_file, 'rb')}
            params['workspaceFileName'] = os.path.basename(workspace_file)
            del params['workspace']

    try:
        r = requests.request(http_method, config.CONFIG_HOST + path,
                             headers={'x-api-key': config.PAPERSPACE_API_KEY},
                             params=params, files=files)
    except requests.exceptions.RequestException as e:
        return requests_exception_to_error_obj(e)

    try:
        return response_error_check(r.json())
    except ValueError:
        return status_code_to_error_obj(r.status_code)


def list(params):
    return method('jobs', 'getJobs', params)


def artifactsList(params):
    return method('jobs', 'artifactsList', params)


def artifactsDestroy(params):
    return method('jobs', 'artifactsDestroy', params)


def show(params):
    return method('jobs', 'getJob', params)


def clone(params):
    return method('jobs', 'clone', params)


def stop(params):
    return method('jobs', 'stop', params)


def destroy(params):
    return method('jobs', 'destroy', params)


def logs(params, tail=False, no_logging=False):
    if 'apiKey' in params:
        config.PAPERSPACE_API_KEY = params['apiKey']
        del params['apiKey']
    elif not config.PAPERSPACE_API_KEY:
        config.PAPERSPACE_API_KEY = apikey()

    last_line = 0
    PSEOF = False
    result = []
    MAX_BACKOFF = 30
    backoff = 0

    if 'line' not in params:
        params['line'] = 0

    while True:
        try:
            r = requests.request('GET', config.CONFIG_LOG_HOST + '/jobs/logs',
                                 headers={'x-api-key': config.PAPERSPACE_API_KEY},
                                 params=params)
        except requests.exceptions.RequestException as e:
            res = requests_exception_to_error_obj(e)
            if no_logging:
                return res
            print_json_pretty(res)
            return False
        else:
            try:
                res = r.json()
                if 'error' in res:
                    if no_logging:
                        return res
                    print_json_pretty(res)
                    if tail:
                        print('Error: logs tail exited before job completed')
                    else:
                        print('Error: logs exited on error')
                    return False

            except ValueError:
                res = []

            if no_logging:
                result += res
            else:
                for l in res:
                    m = l['message']
                    if m != 'PSEOF':
                        print(m)

            if res:
                last_line = res[-1]['line']
                PSEOF = res[-1]['message'] == 'PSEOF'

            if PSEOF:
                break

            if last_line > params['line']:
                params['line'] = last_line
                backoff = 0
                continue

            if tail:
                if backoff:
                    time.sleep(backoff)
                    backoff = min(backoff * 2, MAX_BACKOFF)
                else:
                    backoff = 1
            else:
                break

    if no_logging:
         return result
    return True


def waitfor(params):
    while True:
        job = method('jobs', 'getJob', params)
        if 'state' not in job:
            return job
        state = job['state']

        if (state == params['state']
           or (state == 'Running' and params['state'] == 'Pending')
           or state == 'Error'
           or state == 'Stopped'
           or state == 'Failed'):
            return job
        time.sleep(5)


def create(params, no_logging=False):
    job = method('jobs', 'createJob', params)
    if no_logging:
        return job
    if 'id' not in job:
        print_json_pretty(job)
        return job
    jobId = job['id']
    print('New jobId: %s' % jobId)
    print('Job %s' % job['state'])

    if job['state'] == 'Pending':
        print('Waiting for job to run...')
        job = waitfor({'jobId': jobId, 'state': 'Running'})
        if 'state' not in job:
            print_json_pretty(job)
            return job

    if job['state'] != 'Error':
        print('Awaiting logs...')
        if logs({'jobId': jobId}, tail=True):
            job = method('jobs', 'getJob', {'jobId': jobId})
        else:
            job = waitfor({'jobId': jobId, 'state': 'Stopped'})
        if 'state' not in job:
            print_json_pretty(job)
            return job

    if job['state'] != 'Error':
        print('Job %s; exitCode %d' % (job['state'], job['exitCode']))
    else:
        print('Job %s: %s' % (job['state'], job['jobError']))
    return job


def artifactsGet(params, no_logging=False):
    result = []
    if 'dest' in params:
        dest = os.path.abspath(os.path.expanduser(params['dest']))
        if not os.path.exists(dest):
            os.makedirs(dest)
        else:
            if not os.path.isdir(dest):
                print('Destination path not is not directory: %s' % dest)
                if no_logging:
                    return result
                return False
        del params['dest']
    else:
        dest = os.getcwd()

    artifacts_list = method('jobs', 'artifactsList', params)
    if artifacts_list:

        creds = method('jobs', 'artifactsGet', params)
        if 'bucket' in creds:
            bucket = creds['bucket']
            folder = creds['folder']
            credentials = creds['Credentials']

            session = boto3.Session(
                aws_access_key_id=credentials['AccessKeyId'],
                aws_secret_access_key=credentials['SecretAccessKey'],
                aws_session_token=credentials['SessionToken']
                )
            s3 = session.resource('s3')

            for item in artifacts_list:
                file = item['file']
                dest_file = os.path.join(dest, file)

                dest_dir = os.path.dirname(dest_file)
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)

                key = folder + '/' + file
                if not no_logging:
                    print('Downloading %s' % file)

                try:
                    s3.Bucket(bucket).download_file(key, dest_file)
                except botocore.exceptions.ClientError as e:
                    if e.response['Error']['Code'] == "404":
                        print("The s3 object does not exist: %s" % key)
                    else:
                        raise
                if no_logging:
                    result.append({ 'file': file, 'destination': dest_file })

            if no_logging:
                return result
            print('Download complete')
            return True
        else:
            if no_logging:
                return creds
            print_json_pretty(creds)
            return False

    if no_logging:
        return result
    return False


# TO DO:
# deal with invalid directories, e.g. root for workspace
# detect running interactively
# stream file uploads/downloads


def run(params={}, no_logging=False):
    if 'PS_JOB_RUNNER' in os.environ:
        return

    stack = inspect.stack()
    obj = __import__(stack[1][0].f_globals['__name__'])
    src = inspect.getsource(obj)
    src_file = os.path.basename(inspect.getsourcefile(obj))

    # TO DO: remove these replacements once we are auto importing paperspace on the job runner
    src = src.replace('import paperspace', '# import paperspace')
    src = src.replace('from paperspace', '# from paperspace')
    src = src.replace('paperspace.config.PAPERSPACE_API_KEY', '_paperspace_config_PAPERSPACE_API_KEY')
    src = src.replace('paperspace.config.CONFIG_HOST', '_paperspace_config_CONFIG_HOST')
    src = src.replace('paperspace.config.CONFIG_LOG_HOST', '_paperspace_config_CONFIG_LOG_HOST')
    src = src.replace('paperspace.jobs.run', '_paperspace_null_func')
    src = src.replace('paperspace.run', '_paperspace_null_func')
    src = src.replace('paperspace.login', '_paperspace_null_func')
    src = src.replace('paperspace.logout', '_paperspace_null_func')
    src = "def _paperspace_null_func(*args, **kwargs): return None\n" + src

    src_path = os.path.join(tempfile.gettempdir(), src_file)
    with open(src_path, "w") as file:
        file.write(src)

    if 'project' not in params:
        params['project'] = 'paperspace-python'
    if 'machineType' not in params:
        params['machineType'] = 'GPU+'
    if 'container' not in params:
        params['container'] = 'Test-Container'
    params['command'] = 'python3 ' + src_file
    params['workspace'] = src_path

    create(params, no_logging)
    sys.exit(0)


# TO DO:
# automatic install of imported dependencies
# make console logging optional
# allow return results
# prevent interactive use
# combine local workspace with source
# detect/use python environment

import inspect
import json
import os
import re
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

def zip_to_tmp(files, ignore_files=[]):
    file = files[0]
    zipname = os.path.join(tempfile.gettempdir(),
                           os.path.basename(os.path.abspath(os.path.expanduser(file)))) + '.zip'
    outZipFile = zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED)
    files_added = set()
    with outZipFile:
        for file in files:
            if os.path.isdir(file):
                for dirpath, dirnames, filenames in os.walk(file):
                    dirnames[:] = [d for d in dirnames if d not in ignore_files]
                    for filename in filenames:
                        if filename not in ignore_files:
                            filepath = os.path.join(dirpath, filename)
                            arcname = os.path.relpath(filepath, file)
                            if arcname not in files_added:
                                outZipFile.write(filepath, arcname)
                                files_added.add(arcname)
            else:
                arcname = os.path.basename(file)
                if arcname not in files_added:
                    outZipFile.write(file, arcname)
                    files_added.add(arcname)
    return zipname


def print_json_pretty(res):
    print(json.dumps(res, indent=2, sort_keys=True))


def method(category, method, params):
    params = params.copy()
    if 'apiKey' in params:
        config.PAPERSPACE_API_KEY = params.pop('apiKey')
    elif not config.PAPERSPACE_API_KEY:
        config.PAPERSPACE_API_KEY = apikey()
    params.pop('tail', None)
    no_logging = params.pop('no_logging', None)
    workspace_files = params.pop('extraFiles', [])
    ignore_files = params.pop('ignoreFiles', [])

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

        workspace = params.get('workspace', None)
        ignore_files.extend(['.git', '.gitignore'])
        if workspace:
            if workspace != 'none':
                workspace_files.insert(0, workspace)
                del params['workspace']

        if workspace_files:
            workspace_file = None
            for file in workspace_files:
                file_path = os.path.expanduser(file)
                if not os.path.exists(file_path):
                    message = format('error: file or directory not found: %s' % file_path)
                    print(message)
                    if no_logging:
                        return { 'error': True, 'message': message }
                    sys.exit(1)
                elif file_path == '/':
                    message = 'error: cannot zip root directory'
                    print(message)
                    if no_logging:
                        return { 'error': True, 'message': message }
                    sys.exit(1)

                if len(workspace_files) == 1 and (file_path.endswith('.zip') or file_path.endswith('.gz')):
                    workspace_file = file_path

            if not workspace_file:
                workspace_file = zip_to_tmp(workspace_files, ignore_files)

            files = {'file': open(workspace_file, 'rb')}
            params['workspaceFileName'] = os.path.basename(workspace_file)

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
    params = params.copy()
    if 'apiKey' in params:
        config.PAPERSPACE_API_KEY = params.pop('apiKey')
    elif not config.PAPERSPACE_API_KEY:
        config.PAPERSPACE_API_KEY = apikey()
    tail = params.pop('tail', False) or tail
    no_logging = params.pop('no_logging', False) or no_logging

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
           or state == 'Failed'
           or state == 'Cancelled'):
            return job
        time.sleep(5)


def create(params, no_logging=False, extra_files=[]):
    no_logging = no_logging or params.get('no_logging', False)
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

    if job['state'] != 'Error' and job['state'] != 'Cancelled':
        print('Awaiting logs...')
        if logs({'jobId': jobId}, tail=True):
            job = method('jobs', 'getJob', {'jobId': jobId})
        else:
            job = waitfor({'jobId': jobId, 'state': 'Stopped'})
        if 'state' not in job:
            print_json_pretty(job)
            return job

    if job['state'] == 'Error':
        print('Job %s: %s' % (job['state'], job['jobError']))
    elif job['state'] == 'Cancelled':
        print('Job %s' % (job['state']))
    else:
        print('Job %s; exitCode %d' % (job['state'], job['exitCode']))
    return job


def artifactsGet(params, no_logging=False):
    params = params.copy()
    no_logging = no_logging or params.get('no_logging', False)
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
# detect running interactively
# stream file uploads/downloads


def run(params={}, no_logging=False):
    if 'PS_JOB_RUNNER' in os.environ:
        return

    # handle script is first arg, params is second
    if isinstance(params, str):
        script = params
        if isinstance(no_logging, dict):
            params = no_logging
            no_logging = False
        else:
            params = {}
        params['script'] = script

    params = params.copy()
    run_this = False
    if 'script' not in params:
        run_this = True

        stack = inspect.stack()
        obj = __import__(stack[1][0].f_globals['__name__'])
        src = inspect.getsource(obj)
        src_file = os.path.basename(inspect.getsourcefile(obj))

        # TO DO: remove these replacements once we are auto importing paperspace on the job runner
        src, n = re.subn('^import paperspace', 'def _paperspace_null_func(*args, **kwargs): return None\n#import _paperspace', src, count=1, flags=re.MULTILINE)
        if n != 0:
            src = re.sub('^import paperspace*$', '', src, flags=re.MULTILINE)
            src = re.sub('import paperspace', 'pass #import _paperspace', src)
            src = re.sub('^from paperspace', '#from _paperspace', src, flags=re.MULTILINE)
            src = re.sub('from paperspace', 'pass #from _paperspace', src)
            src = src.replace('paperspace.config.PAPERSPACE_API_KEY', '_paperspace_config_PAPERSPACE_API_KEY')
            src = src.replace('paperspace.config.CONFIG_HOST', '_paperspace_config_CONFIG_HOST')
            src = src.replace('paperspace.config.CONFIG_LOG_HOST', '_paperspace_config_CONFIG_LOG_HOST')
            src = src.replace('paperspace.jobs.run', '_paperspace_null_func')
            src = src.replace('paperspace.run', '_paperspace_null_func')
            src = src.replace('paperspace.login', '_paperspace_null_func')
            src = src.replace('paperspace.logout', '_paperspace_null_func')

        src_path = os.path.join(tempfile.gettempdir(), src_file)
        with open(src_path, "w") as file:
            file.write(src)
    else:
        src_file = os.path.basename(params['script'])
        src_path = params.pop('script')

    if 'project' not in params:
        params['project'] = 'paperspace-python'
    if 'machineType' not in params:
        params['machineType'] = 'P5000'
    if 'container' not in params:
        params['container'] = 'paperspace/tensorflow-python'

    python_ver = params.pop('python', str(sys.version_info[0])) # defaults locally running version
    # TODO validate python version; handle no version, specific version

    if 'command' not in params:
         params['command'] = 'python' + python_ver + ' ' + src_file

    if not os.path.exists(src_path):
        message = format('error: file not found: %s' % src_path)
        print(message)
        if 'no_logging' in params:
            return { 'error': True, 'message': message }
        sys.exit(1)
    elif os.path.isdir(src_path):
        message = format('error: specified file is a directory: %s' % src_path)
        print(message)
        if 'no_logging' in params:
            return { 'error': True, 'message': message }
        sys.exit(1)

    params['extraFiles'] = []
    if 'workspace' not in params:
        params['workspace'] = src_path
    else:
        params['extraFiles'].append(src_path)

    if 'ignoreFiles' in params:
        if isinstance(params['ignoreFiles'], str):
            params['ignoreFiles'] = params['ignoreFiles'].split(',')

    req = params.pop('req', None)
    if req:
        if not isinstance(req, str):
            req = 'requirements.txt'
        if os.path.exists(req):
            params['extraFiles'].append(req)
        params['command'] = 'pip' + python_ver + ' install -r ' + os.path.basename(req) + '\n' + params['command']

    pipenv = params.pop('pipenv', None)
    if pipenv:
        for pipfile in ['Pipfile', 'Pipfile.lock']:
            if os.path.exists(pipfile):
                params['extraFiles'].append(pipfile)
        uses_python_ver = ''
        if python_ver.startswith('3'):
            uses_python_ver == '--three '
        elif python_ver.startswith('2'):
            uses_python_ver == '--two '
        params['command'] = 'pipenv ' + uses_python_ver + 'install\n' + params['command']

    conda = params.pop('conda', None)
    if conda:
        params['command'] = 'conda -env ' + conda + '\n' + params['command']

    init = params.pop('init', None)
    if init:
        if not isinstance(init, str):
            init = 'init.sh'
        if os.path.exists(init):
            params['extraFiles'].append(init)
        params['command'] = '. ' + os.path.basename(init) + '\n' + params['command']

    res = create(params, no_logging)
    if run_this:
        sys.exit(0)
    return res


# TO DO:
# automatic install of imported dependencies
# allow return results
# detect/use python environment

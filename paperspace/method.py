import json
import os
import subprocess
import sys
import tempfile
import zipfile

import requests

from paperspace import logger
from .config import config
from .version import version


def zip_to_tmp(files, ignore_files=[]):
    file = files[0]
    zipname = os.path.join(tempfile.gettempdir(),
                           os.path.basename(os.path.abspath(os.path.expanduser(file)))) + '.zip'
    outZipFile = zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED)
    files_added = set()
    with outZipFile:
        for file in files:
            file = os.path.abspath(os.path.expanduser(file))
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
        config.PAPERSPACE_API_KEY = get_apikey()
    params.pop('tail', None)
    no_logging = params.pop('no_logging', None)
    workspace_files = params.pop('extraFiles', [])
    ignore_files = params.pop('ignoreFiles', [])

    if category == 'jobs' and method in ['artifactsGet', 'artifactsList', 'getJob', 'getJobs', 'getLogs', 'getClusterAvailableMachineTypes']:
        http_method = 'GET'
        path = '/' + category + '/' + method

    elif category == 'jobs' and method in ['artifactsDestroy', 'clone', 'destroy', 'stop']:
        http_method = 'POST'
        path = '/' + category + '/' + params['jobId'] + '/' + method
        del params['jobId']

    elif ((category == 'machines' and method in ['getAvailability', 'getMachines', 'getMachinePublic', 'getUtilization'])
        or (category == 'scripts' and method in ['getScript', 'getScripts', 'getScriptText'])
        or (category == 'networks' and method == 'getNetworks')
        or (category == 'templates' and method == 'getTemplates')
        or (category == 'users' and method == 'getUsers')):
        http_method = 'GET'
        path = '/' + category + '/' + method

    elif category == 'machines' and method in ['destroyMachine', 'restart', 'start', 'stop', 'updateMachinePublic']:
        http_method = 'POST'
        path = '/' + category + '/' + params['machineId'] + '/' + method

    elif category == 'scripts' and method == 'destroy':
        http_method = 'POST'
        path = '/' + category + '/' + params['scriptId'] + '/' + method
        del params['scriptId']

    else:
        http_method = 'POST'
        path = '/' + category + '/' + method

    files = None
    if method == 'createJob' and 'workspace' in params:
        workspace = params.get('workspace', None)
        if workspace[:1] == '~':
             workspace = os.path.expanduser(workspace)
        if workspace.find("$") != -1:
             workspace = os.path.expandvars(workspace)
        if os.path.isdir(os.path.abspath(workspace)+"/.git"):
            try:
                git_short_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], cwd=os.path.abspath(workspace)).strip()
                code_commit = git_short_hash.decode("utf-8")
                params['codeCommit'] = code_commit
            except Exception as e:
                pass
        ignore_files.extend(['.git', '.gitignore', '__pycache__'])
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
                    if no_logging:
                        return { 'error': True, 'message': message }
                    print(message)
                    sys.exit(1)
                elif file_path == '/':
                    message = 'error: cannot zip root directory'
                    if no_logging:
                        return { 'error': True, 'message': message }
                    print(message)
                    sys.exit(1)

                if len(workspace_files) == 1 and (file_path.endswith('.zip') or file_path.endswith('.gz')):
                    workspace_file = file_path

            if not workspace_file:
                workspace_file = zip_to_tmp(workspace_files, ignore_files)

            files = {'file': open(workspace_file, 'rb')}
            params['workspaceFileName'] = os.path.basename(workspace_file)

    try:
        data = None
        if category == 'machines' and method == 'createSingleMachinePublic':
            data = params
            params = None
        url = config.CONFIG_HOST + path
        headers = {'x-api-key': config.PAPERSPACE_API_KEY, 'ps_client_name': 'paperspace-python',
                   'ps_client_version': version}
        r = requests.request(http_method, url, headers=headers, params=params, data=data, files=files)
        logger.debug("{} request sent to: {} with headers: {} params: {} data: {} files: {}"
                     .format(http_method, url, headers, params, data, files))
    except requests.exceptions.RequestException as e:
        return requests_exception_to_error_obj(e)

    try:
        if r.status_code != 204:
            return response_error_check(r.json())
        else:
            return {}
    except ValueError:
        return status_code_to_error_obj(r.status_code)


def response_error_check(res):
    if ('error' not in res
        and 'status' in res
        and (res['status'] < 200 or res['status'] > 299)):
        res['error'] = True
    return res


def requests_exception_to_error_obj(e):
    return { 'error': True, 'message': str(e) }


def status_code_to_error_obj(status_code):
    message = 'unknown'
    if status_code in requests.status_codes._codes:
        message = requests.status_codes._codes[status_code][0]
    return { 'error': True, 'message': message, 'status': status_code }


def get_apikey():
    paperspace_dir = os.path.expanduser('~/.paperspace')
    config_path = os.path.join(paperspace_dir, 'config.json')
    if os.path.exists(config_path):
        config_data = json.load(open(config_path))
        if config_data and 'apiKey' in config_data:
            return config_data['apiKey']
    return ''

import requests
import json
import time
import os
import zipfile
import tempfile

PAPERSPACE_API_KEY = '14a4bc1cbc414...'
CONFIG_HOST = 'https://api.paperspace.io'
CONFIG_LOG_HOST = 'https://logs.paperspace.io'

def print_json_pretty(res):
	print(json.dumps(res, indent = 2, sort_keys = True))

def paperspace(category, method, params):

	if method in ['artifactsGet', 'artifactsList', 'getJob', 'getJobs', 'getLogs']:

		http_method = 'GET'
		path = '/' + category + '/' + method

	elif method in ['artifactsDestroy', 'clone', 'destroy', 'stop']:

		http_method = 'POST'
		path = '/' + category + '/' + params['jobId'] + '/' + method
		del params['jobId']

	else:

		http_method = 'POST'
		path = '/' + category + '/' + method

	r = requests.request(http_method, CONFIG_HOST + path, headers = {'x-api-key': PAPERSPACE_API_KEY }, params = params)

	return r.json()

res = paperspace('jobs', 'getJobs', {'project': 'paperspace-node'})
for e in res:
	print(e['id'])

res = paperspace('jobs', 'getJob', {'jobId': 'j8eww41akg9h0'})
print(res['state'])
print_json_pretty(res)

res = paperspace('jobs', 'stop', {'jobId': 'j8eww41akg9h0'})
print_json_pretty(res)

#res = paperspace('jobs', 'clone', {'jobId': 'j8eww41akg9h0'})
#print_json_pretty(res)

#res = paperspace('jobs', 'createJob', {'project': 'paperspace-python',
#	'workspace':'none', 'machineType': 'GPU+', 'container': 'Test-Container'})
#print_json_pretty(res)

def paperspace_jobs_logs(params, tail = False, json = False):
	last_line = 0
	PSEOF = False
	json_res = []
	MAX_BACKOFF = 30
	backoff = 0

	if 'line' not in params:
		params['line'] = 0

	while True:
		r = requests.request('GET', CONFIG_LOG_HOST + '/jobs/logs', headers = {'x-api-key': PAPERSPACE_API_KEY }, params = params)
		try:
			res = r.json()
		except ValueError:
			res = []
		if json:
			json_res += res
		else:
			for l in res:
				m = l['message']
				if m != 'PSEOF':
					print(m)

		if len(res):
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

	if json:
		print_json_pretty(json_res)

paperspace_jobs_logs({'jobId': 'jsjo03tmsh6kzy', 'limit': 4}, tail = True)

def zip(obj_name):
	zipname = os.path.join(tempfile.gettempdir(), os.path.basename(obj_name)) + '.zip'
	outZipFile = zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED)
	if os.path.isdir(obj_name):
		for dirpath, dirnames, filenames in os.walk(obj_name):
			for filename in dirnames + filenames:
				filepath = os.path.join(dirpath, filename)
				basename = os.path.basename(filepath)
				if '/.git/' not in filepath and basename not in ['.git', '.gitignore']:
					arcname = os.path.relpath(filepath, obj_name)
					outZipFile.write(filepath, arcname)
	else:
		outZipFile.write(obj_name)
	outZipFile.close()
	return zipname

workspace = '~/myproject3'
#workspace = 'paperspace.py'
#workspace = None

workspace_file = None
if workspace and workspace != 'none':
	workspace_path = os.path.expanduser(workspace)
	if os.path.exists(workspace_path):
		if not workspace_path.endswith('.zip') and not workspace_path.endswith('.gz'):
			workspace_file = zip(workspace_path)
		else:
			workspace_file = workspace_path

if workspace_file:
	# add workspace_file to POST
	print(workspace_file)

# TODO: 
# upload a workspace folder
# download artifacts
# create/use project config
# deal with timeouts/server unreachable

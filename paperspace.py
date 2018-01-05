import requests
import json
import time
import os
import zipfile
import tempfile

PAPERSPACE_API_KEY = '14a4bc1cbc414...'
CONFIG_HOST = 'https://api.paperspace.io'
CONFIG_LOG_HOST = 'https://logs.paperspace.io'

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

	files = None
	if method == 'createJob' and 'workspace' in params:
		workspace = params['workspace']
		workspace_file = None
		if workspace and workspace != 'none':
			workspace_path = os.path.expanduser(workspace)
			if os.path.exists(workspace_path):
				if not workspace_path.endswith('.zip') and not workspace_path.endswith('.gz'):
					workspace_file = zip(workspace_path)
				else:
					workspace_file = workspace_path
			files = {'file': open(workspace_file, 'rb')}
			params['workspaceFileName'] = os.path.basename(workspace_file)
			del params['workspace']

	r = requests.request(http_method, CONFIG_HOST + path, headers = {'x-api-key': PAPERSPACE_API_KEY }, params = params, files = files)

	return r.json()

#Tests:

#jobs = paperspace('jobs', 'getJobs', {'project': 'paperspace-node'})
#for job in jobs:
#	print(job['id'])

#job = paperspace('jobs', 'getJob', {'jobId': 'j8eww41akg9h0'})
#print(job['state'])
#print_json_pretty(job)

#job = paperspace('jobs', 'stop', {'jobId': 'j8eww41akg9h0'})
#print_json_pretty(job)

#job = paperspace('jobs', 'clone', {'jobId': 'j8eww41akg9h0'})
#print_json_pretty(job)

#job = paperspace('jobs', 'createJob', {'project': 'paperspace-python',
#	'workspace':'none', 'machineType': 'GPU+', 'container': 'Test-Container'})
#print_json_pretty(job)

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

#Test
#paperspace_jobs_logs({'jobId': 'jsjo03tmsh6kzy', 'limit': 4}, tail = True)

def paperspace_jobs_waitfor(params):
	while True:
		job = paperspace('jobs', 'getJob', params)
		state = job['state']
		if state == params['state'] or \
			(state == 'Running' and params['state'] == 'Pending') or \
			state == 'Error' or \
			state == 'Stopped' or \
			state == 'Failed':
			return job
		time.sleep(5)

def paperspace_jobs_create(params):
	job = paperspace('jobs', 'createJob', params)
	jobId = job['id']
	print_json_pretty(job)
	print("New jobId: %s" % jobId)
	print("Job %s" % job['state'])

	if job['state'] == 'Pending':
		print('Waiting for job to run...')
		job = paperspace_jobs_waitfor({'jobId': jobId, 'state': 'Running'})

	if job['state'] != 'Error':
		print('Awaiting logs...')
		paperspace_jobs_logs({'jobId': jobId}, tail = True)
		job = paperspace('jobs', 'getJob', {'jobId': jobId})

	if job['state'] != 'Error':
		print("Job %s; exitCode %d" % (job['state'], job['exitCode']))
	else:
		print("Job %s: %s" % (job['state'], job['jobError'])

#Test
paperspace_jobs_create({'project': 'myproject3',
	'machineType': 'GPU+', 'container': 'Test-Container',
	'command': './do.sh', 'workspace': '~/myproject3'})

# TODO:
# download artifacts
# create/use project config
# deal with timeouts/server unreachable

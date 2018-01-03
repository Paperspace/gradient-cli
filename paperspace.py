import requests
import json

PAPERSPACE_API_KEY = '14a4bc1cbc414...'
CONFIG_HOST = 'https://api.paperspace.io'

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

res = paperspace('jobs', 'stop', {'jobId': 'j8eww41akg9h0'})
print(res)

res = paperspace('jobs', 'clone', {'jobId': 'j8eww41akg9h0'})
print_json_pretty(res)

res = paperspace('jobs', 'createJob', {'project': 'paperspace-python',
	'workspace':'none', 'machineType': 'GPU+', 'container': 'Test-Container'})
print_json_pretty(res)

# TODO: 
# get logs
# zip and upload a workspace folder
# download artifacts
# create/use project config
# deal with timeouts/server unreachable
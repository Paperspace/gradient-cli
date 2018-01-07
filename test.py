import paperspace

# Tests:

paperspace.PAPERSPACE_API_KEY = '14a4bc1cbc414...'

project = 'myproject7'
print('project: %s' % project)

print("paperspace.paperspace('jobs', 'getJobs', {'project': project})")
jobs = paperspace.paperspace('jobs', 'getJobs', {'project': project})
if 'error' in jobs:
    paperspace.print_json_pretty(jobs)
else:
    for job in jobs:
        print(job['id'])

print("jobs_create({'project': project, 'machineType': 'GPU+', 'container': 'Test-Container', 'command': './do.sh', 'workspace': '~/myproject3'})")
job = paperspace.jobs_create({'project': project,
                              'machineType': 'GPU+', 'container': 'Test-Container',
                              'command': './do.sh', 'workspace': '~/myproject3'})
jobId = job['id']

print("paperspace.paperspace('jobs', 'artifactsList', {'jobId': jobId, 'links': True})")
artifacts = paperspace.paperspace('jobs', 'artifactsList', {'jobId': jobId, 'links': True})
if artifacts:
    paperspace.print_json_pretty(artifacts)

print("paperspace.jobs_artifactsGet({'jobId': jobId, 'dest': '~/temp1'})")
paperspace.jobs_artifactsGet({'jobId': jobId, 'dest': '~/temp1'})

print("paperspace.paperspace('jobs', 'getJob', {'jobId': jobId})")
job = paperspace.paperspace('jobs', 'getJob', {'jobId': jobId})
paperspace.print_json_pretty(job)

print("paperspace.jobs_logs({'jobId': jobId, 'limit': 4}, tail=True)")
paperspace.jobs_logs({'jobId': jobId, 'limit': 4}, tail=True)

print("paperspace.paperspace('jobs', 'stop', {'jobId': jobId})")
res = paperspace.paperspace('jobs', 'stop', {'jobId': jobId})
paperspace.print_json_pretty(res)

print("paperspace.paperspace('jobs', 'clone', {'jobId': jobId})")
clonedJob = paperspace.paperspace('jobs', 'clone', {'jobId': jobId})
paperspace.print_json_pretty(clonedJob)

print("paperspace.jobs_waitfor({'jobId': clonedJob['id'], 'state': 'Stopped'})")
waitforJob = paperspace.jobs_waitfor({'jobId': clonedJob['id'], 'state': 'Stopped'})
paperspace.print_json_pretty(waitforJob)

print("paperspace.paperspace('jobs', 'artifactsList', {'jobId': clonedJob['id']})")
artifacts = paperspace.paperspace('jobs', 'artifactsList', {'jobId': clonedJob['id']})
if artifacts:
    paperspace.print_json_pretty(artifacts)
    print("paperspace.paperspace('jobs', 'artifactsDestroy', {'jobId': clonedJob['id']})")
    paperspace.paperspace('jobs', 'artifactsDestroy', {'jobId': clonedJob['id']})

    print("paperspace.paperspace('jobs', 'artifactsList', {'jobId': clonedJob['id']})")
    artifacts = paperspace.paperspace('jobs', 'artifactsList', {'jobId': clonedJob['id']})
    if artifacts:
        paperspace.print_json_pretty(artifacts)

print("paperspace.paperspace('jobs', 'getJobs', {'project': project})")
jobs = paperspace.paperspace('jobs', 'getJobs', {'project': project})
for job in jobs:
    print(job['id'])

print("paperspace.paperspace('jobs', 'destroy', {'jobId': clonedJob['id']})")
res = paperspace.paperspace('jobs', 'destroy', {'jobId': clonedJob['id']})
paperspace.print_json_pretty(res)

print("paperspace.paperspace('jobs', 'getJobs', {'project': project})")
jobs = paperspace.paperspace('jobs', 'getJobs', {'project': project})
for job in jobs:
    print(job['id'])

import paperspace

# Tests:

paperspace.config.PAPERSPACE_API_KEY = '14a4bc1cbc414...'

project = 'myproject'
print('project: %s' % project)

print("paperspace.jobs.getJobs({'project': project})")
jobs = paperspace.jobs.getJobs({'project': project})
if 'error' in jobs:
    paperspace.jobs.print_json_pretty(jobs)
else:
    for job in jobs:
        print(job['id'])

print("jobs.create({'project': project, 'machineType': 'GPU+', 'container': 'Test-Container', 'command': './do.sh', 'workspace': '~/myproject3'})")
job = paperspace.jobs.create({'project': project,
                              'machineType': 'GPU+', 'container': 'Test-Container',
                              'command': './do.sh', 'workspace': '~/myproject3'})
jobId = job['id']

print("paperspace.jobs.artifactsList({'jobId': jobId, 'links': True})")
artifacts = paperspace.jobs.artifactsList({'jobId': jobId, 'links': True})
if artifacts:
    paperspace.jobs.print_json_pretty(artifacts)

print("paperspace.jobs.artifactsGet({'jobId': jobId, 'dest': '~/temp1'})")
paperspace.jobs.artifactsGet({'jobId': jobId, 'dest': '~/temp1'})

print("paperspace.jobs.getJob({'jobId': jobId})")
job = paperspace.jobs.getJob({'jobId': jobId})
paperspace.jobs.print_json_pretty(job)

print("paperspace.jobs.logs({'jobId': jobId, 'limit': 4}, tail=True)")
paperspace.jobs.logs({'jobId': jobId, 'limit': 4}, tail=True)

print("paperspace.jobs.stop({'jobId': jobId})")
res = paperspace.jobs.stop({'jobId': jobId})
paperspace.jobs.print_json_pretty(res)

print("paperspace.jobs.clone({'jobId': jobId})")
clonedJob = paperspace.jobs.clone({'jobId': jobId})
paperspace.jobs.print_json_pretty(clonedJob)

print("paperspace.jobs.waitfor({'jobId': clonedJob['id'], 'state': 'Stopped'})")
waitforJob = paperspace.jobs.waitfor({'jobId': clonedJob['id'], 'state': 'Stopped'})
paperspace.jobs.print_json_pretty(waitforJob)

print("paperspace.jobs.artifactsList({'jobId': clonedJob['id']})")
artifacts = paperspace.jobs.artifactsList({'jobId': clonedJob['id']})
if artifacts:
    paperspace.jobs.print_json_pretty(artifacts)
    print("paperspace.jobs.artifactsDestroy({'jobId': clonedJob['id']})")
    paperspace.jobs.artifactsDestroy({'jobId': clonedJob['id']})

    print("paperspace.jobs.artifactsList({'jobId': clonedJob['id']})")
    artifacts = paperspace.jobs.artifactsList({'jobId': clonedJob['id']})
    if artifacts:
        paperspace.jobs.print_json_pretty(artifacts)

print("paperspace.jobs.getJobs({'project': project})")
jobs = paperspace.jobs.getJobs({'project': project})
for job in jobs:
    print(job['id'])

print("paperspace.jobs.destroy({'jobId': clonedJob['id']})")
res = paperspace.jobs.destroy({'jobId': clonedJob['id']})
paperspace.jobs.print_json_pretty(res)

print("paperspace.jobs.getJobs({'project': project})")
jobs = paperspace.jobs.getJobs({'project': project})
for job in jobs:
    print(job['id'])

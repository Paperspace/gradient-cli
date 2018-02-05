import sys
import paperspace

# Tests:

project = 'myproject'
print('project: %s' % project)

def errorcheck(res):
    if 'error' in res:
        paperspace.print_json_pretty(res)
        sys.exit(1)

print("paperspace.jobs.list({'project': project})")
jobs = paperspace.jobs.list({'project': project})
errorcheck(jobs)
for job in jobs:
    print(job['id'])

print("jobs.create({'project': project, 'machineType': 'GPU+', 'container': 'Test-Container', 'command': './do.sh', 'workspace': '~/myproject3'})")
job = paperspace.jobs.create({'project': project,
                              'machineType': 'GPU+', 'container': 'Test-Container',
                              'command': './do.sh', 'workspace': '~/myproject3'})
errorcheck(job)
jobId = job['id']

print("paperspace.jobs.artifactsList({'jobId': jobId, 'links': True})")
artifacts = paperspace.jobs.artifactsList({'jobId': jobId, 'links': True})
errorcheck(artifacts)
if artifacts:
    paperspace.print_json_pretty(artifacts)

print("paperspace.jobs.artifactsGet({'jobId': jobId, 'dest': '~/temp1'})")
if not paperspace.jobs.artifactsGet({'jobId': jobId, 'dest': '~/temp1'}):
    print('paperspace.jobs.artifactsGet returned False')
    sys.exit(1)

print("paperspace.jobs.show({'jobId': jobId})")
job = paperspace.jobs.show({'jobId': jobId})
paperspace.print_json_pretty(job)

print("paperspace.jobs.logs({'jobId': jobId, 'limit': 4}, tail=True)")
if not paperspace.jobs.logs({'jobId': jobId, 'limit': 4}, tail=True):
    print('logs encountered an error')

print("paperspace.jobs.logs({'jobId': jobId, 'limit': 4}, no_logging=True)")
res = paperspace.jobs.logs({'jobId': jobId, 'limit': 4}, no_logging=True)
paperspace.print_json_pretty(res)

print("paperspace.jobs.stop({'jobId': jobId})")
res = paperspace.jobs.stop({'jobId': jobId})
paperspace.print_json_pretty(res)

print("paperspace.jobs.clone({'jobId': jobId})")
clonedJob = paperspace.jobs.clone({'jobId': jobId})
paperspace.print_json_pretty(clonedJob)

print("paperspace.jobs.waitfor({'jobId': clonedJob['id'], 'state': 'Stopped'})")
waitforJob = paperspace.jobs.waitfor({'jobId': clonedJob['id'], 'state': 'Stopped'})
paperspace.print_json_pretty(waitforJob)

print("paperspace.jobs.artifactsList({'jobId': clonedJob['id']})")
artifacts = paperspace.jobs.artifactsList({'jobId': clonedJob['id']})
errorcheck(artifacts)
if artifacts:
    paperspace.print_json_pretty(artifacts)
    print("paperspace.jobs.artifactsDestroy({'jobId': clonedJob['id']})")
    paperspace.jobs.artifactsDestroy({'jobId': clonedJob['id']})

    print("paperspace.jobs.artifactsList({'jobId': clonedJob['id']})")
    artifacts = paperspace.jobs.artifactsList({'jobId': clonedJob['id']})
    errorcheck(artifacts)
    if artifacts:
        paperspace.print_json_pretty(artifacts)

print("paperspace.jobs.list({'project': project})")
jobs = paperspace.jobs.list({'project': project})
errorcheck(jobs)
for job in jobs:
    print(job['id'])

print("paperspace.jobs.destroy({'jobId': clonedJob['id']})")
res = paperspace.jobs.destroy({'jobId': clonedJob['id']})
paperspace.print_json_pretty(res)

print("paperspace.jobs.list({'project': project})")
jobs = paperspace.jobs.list({'project': project})
errorcheck(jobs)
for job in jobs:
    print(job['id'])

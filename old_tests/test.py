import sys
import paperspace

# Tests:

project = 'all'
print('project: %s' % project)

def errorcheck(res):
    if 'error' in res:
        paperspace.print_json_pretty(res)
        sys.exit(1)


print("paperspace.jobs.machineTypes()")
machineTypes = paperspace.jobs.machineTypes()
errorcheck(machineTypes)
paperspace.print_json_pretty(machineTypes)

print("paperspace.jobs.list({'project': '%s'})" % project)
jobs = paperspace.jobs.list({'project': project})
errorcheck(jobs)
for job in jobs:
    print(job['id'])

print("jobs.create({'project': '%s', 'machineType': 'P5000', 'container': 'paperspace/tensorflow-python', 'command': './do.sh', 'workspace': '~/myproject3', 'cluster': 'Gradient-Node'})" % project)
job = paperspace.jobs.create({'project': project,
                              'machineType': 'P5000', 'container': 'paperspace/tensorflow-python',
                              'command': './do.sh', 'workspace': '~/myproject3'})
if 'error' in job:
    sys.exit(1)
jobId = job['id']

print("paperspace.jobs.artifactsList({'jobId': '%s', 'links': True})" % jobId)
artifacts = paperspace.jobs.artifactsList({'jobId': jobId, 'links': True})
errorcheck(artifacts)
if artifacts:
    paperspace.print_json_pretty(artifacts)

print("paperspace.jobs.artifactsGet({'jobId': '%s', 'dest': '~/temp1'})" % jobId)
if not paperspace.jobs.artifactsGet({'jobId': jobId, 'dest': '~/temp1'}):
    print('paperspace.jobs.artifactsGet returned False')
    sys.exit(1)

print("paperspace.jobs.show({'jobId': '%s'})" % jobId)
job = paperspace.jobs.show({'jobId': jobId})
paperspace.print_json_pretty(job)

print("paperspace.jobs.logs({'jobId': '%s', 'limit': 4}, tail=True)" % jobId)
if not paperspace.jobs.logs({'jobId': jobId, 'limit': 4}, tail=True):
    print('logs encountered an error')

print("paperspace.jobs.logs({'jobId': '%s', 'limit': 4}, no_logging=True)" % jobId)
res = paperspace.jobs.logs({'jobId': jobId, 'limit': 4}, no_logging=True)
paperspace.print_json_pretty(res)

print("paperspace.jobs.stop({'jobId': '%s'})" % jobId)
res = paperspace.jobs.stop({'jobId': jobId})
paperspace.print_json_pretty(res)

print("paperspace.jobs.clone({'jobId': '%s'})" % jobId)
clonedJob = paperspace.jobs.clone({'jobId': jobId})
paperspace.print_json_pretty(clonedJob)

print("paperspace.jobs.waitfor({'jobId': '%s', 'state': 'Stopped'})" % clonedJob['id'])
waitforJob = paperspace.jobs.waitfor({'jobId': clonedJob['id'], 'state': 'Stopped'})
paperspace.print_json_pretty(waitforJob)

print("paperspace.jobs.artifactsList({'jobId': '%s'})" % clonedJob['id'])
artifacts = paperspace.jobs.artifactsList({'jobId': clonedJob['id']})
errorcheck(artifacts)
if artifacts:
    paperspace.print_json_pretty(artifacts)
    print("paperspace.jobs.artifactsDestroy({'jobId': '%s'})" % clonedJob['id'])
    paperspace.jobs.artifactsDestroy({'jobId': clonedJob['id']})

    print("paperspace.jobs.artifactsList({'jobId': '%s'})" % clonedJob['id'])
    artifacts = paperspace.jobs.artifactsList({'jobId': clonedJob['id']})
    errorcheck(artifacts)
    if artifacts:
        paperspace.print_json_pretty(artifacts)

print("paperspace.jobs.list({'project': '%s'})" % project)
jobs = paperspace.jobs.list({'project': project})
errorcheck(jobs)
for job in jobs:
    print(job['id'])

print("paperspace.jobs.destroy({'jobId': '%s'})" % clonedJob['id'])
res = paperspace.jobs.destroy({'jobId': clonedJob['id']})
paperspace.print_json_pretty(res)

print("paperspace.jobs.list({'project': '%s'})" % project)
jobs = paperspace.jobs.list({'project': project})
errorcheck(jobs)
for job in jobs:
    print(job['id'])

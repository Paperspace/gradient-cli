import sys
import paperspace

if not paperspace.login():
    sys.exit(1)

print("paperspace.jobs.list({'project': 'all'})")
jobs = paperspace.jobs.list({'project': 'all'})
if 'error' in jobs:
    paperspace.print_json_pretty(jobs)
else:
    for job in jobs:
        print(job['id'])

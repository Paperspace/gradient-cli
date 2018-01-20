import paperspace

print("paperspace.jobs.artifactsGet({'jobId': 'j4xmmzcy83znb', 'dest': '~/temp1'}, no_logging=True)")
files = paperspace.jobs.artifactsGet({'jobId': 'j4xmmzcy83znb', 'dest': '~/temp1'}, no_logging=True)
paperspace.print_json_pretty(files)

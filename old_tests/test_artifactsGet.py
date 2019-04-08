import paperspace

print("paperspace.jobs.artifactsGet({'jobId': 'jszkrgijy8ethy', 'dest': '~/temp1'}, no_logging=True)")
files = paperspace.jobs.artifactsGet({'jobId': 'jszkrgijy8ethy', 'dest': '~/temp1'}, no_logging=True)
paperspace.print_json_pretty(files)

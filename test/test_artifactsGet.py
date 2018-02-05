import paperspace

print("paperspace.jobs.artifactsGet({'jobId': 'j991w8vlna7u2', 'dest': '~/temp1'}, no_logging=True)")
files = paperspace.jobs.artifactsGet({'jobId': 'j991w8vlna7u2', 'dest': '~/temp1'}, no_logging=True)
paperspace.print_json_pretty(files)

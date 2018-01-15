import os
import paperspace

paperspace.config.PAPERSPACE_API_KEY = '14a4bc1cbc414...'

paperspace.jobs.runas_job({'project': 'myprojec', 'machineType': 'GPU+', 'container': 'Test-Container'})

print(os.getcwd())
print('something useful')

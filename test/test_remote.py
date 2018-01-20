import os
import paperspace

paperspace.jobs.runas_job({'project': 'myproject', 'machineType': 'GPU+', 'container': 'Test-Container'})

print(os.getcwd())
print('something useful')

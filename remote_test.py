import os
import paperspace

paperspace.PAPERSPACE_API_KEY = '14a4bc1cbc414...'

paperspace.runas_job({'project': 'myprojec8', 'machineType': 'GPU+', 'container': 'Test-Container'})

print(os.getcwd())
print('something useful')

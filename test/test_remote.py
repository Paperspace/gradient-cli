import os
import paperspace

paperspace.run({'project': 'myproject', 'machineType': 'GPU+', 'container': 'Test-Container'})

print(os.getcwd())
print('something useful')

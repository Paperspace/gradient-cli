import os
import paperspace

paperspace.run({'project': 'myproject', 'machineType': 'P5000', 'container': 'paperspace/tensorflow-python'})

print(os.getcwd())
print('something useful')

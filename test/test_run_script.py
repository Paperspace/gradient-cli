#invoke with python, not paperspace-python run
import paperspace

print("paperspace.run('myscript.py', {'project': 'myproject', 'machineType': 'P5000', 'container': 'paperspace/tensorflow-python'})")
paperspace.run('myscript.py', {'project': 'myproject', 'machineType': 'P5000', 'container': 'paperspace/tensorflow-python'})
print('test_run_script completed')

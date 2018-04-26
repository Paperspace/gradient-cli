import sys
import time
import paperspace

def errorcheck(res):
    if 'error' in res:
        paperspace.print_json_pretty(res)
        sys.exit(1)
"""
print("paperspace.machines.availability({'region': 'East Coast (NY2)', 'machineType': 'P4000'})")
res = paperspace.machines.availability({'region': 'East Coast (NY2)', 'machineType': 'P4000'})
errorcheck(res)
paperspace.print_json_pretty(res)

print("paperspace.networks.list()")
networks = paperspace.networks.list()
if 'error' in res:
    paperspace.print_json_pretty(res)
else:
    for network in networks:
        paperspace.print_json_pretty(network)

print("paperspace.templates.list()")
templates = paperspace.templates.list()
errorcheck(templates)
for template in templates:
    paperspace.print_json_pretty(template)

print("paperspace.users.list()")
users = paperspace.users.list()
errorcheck(users)
for user in users:
    paperspace.print_json_pretty(user)

print("paperspace.scripts.create(...)")
script = paperspace.scripts.create({'scriptName': 'My Python Script', 'scriptText': 'python --version'})
errorcheck(script)
paperspace.print_json_pretty(script)
scriptId = script['id']

print("paperspace.scripts.show(...)")
script = paperspace.scripts.show({'scriptId': scriptId})
errorcheck(script)
paperspace.print_json_pretty(script)

print("paperspace.scripts.destroy(...)")
res = paperspace.scripts.destroy({'scriptId': scriptId})
errorcheck(res)
paperspace.print_json_pretty(res)

print("paperspace.scripts.list()")
scripts = paperspace.scripts.list()
errorcheck(scripts)
scriptId = None
last_script = None
for script in scripts:
    #paperspace.print_json_pretty(script)
    scriptId = script['id']
    last_script = script
if last_script:
    paperspace.print_json_pretty(last_script)

print("paperspace.scripts.show(...)")
script = paperspace.scripts.show({'scriptId': scriptId})
errorcheck(script)
paperspace.print_json_pretty(script)

print("paperspace.scripts.text(...)")
script = paperspace.scripts.text({'scriptId': scriptId})
errorcheck(script)
paperspace.print_json_pretty(script)

print("paperspace.machines.create(...)")
machine = paperspace.machines.create({'machineType': 'C1', 'region': 'East Coast (NY2)', 'billingType': 'hourly',
    'machineName': 'pythoncreate4', 'templateId': 'tqalmii', 'size': '50', 'dynamicPublicIp': True}) #prod: 'tbludl2'
errorcheck(machine)
paperspace.print_json_pretty(machine)

machineId = machine['id']

machine = paperspace.machines.waitfor({'machineId': machineId, 'state': 'ready'})
errorcheck(machine)
paperspace.print_json_pretty(machine)

print("paperspace.machines.show(...)")
machine = paperspace.machines.show({'machineId': machineId})
errorcheck(machine)
paperspace.print_json_pretty(machine)

print("paperspace.machines.list()")
machines = paperspace.machines.list()
errorcheck(machines)
paperspace.print_json_pretty(machine)
found = False
for machine in machines:
    if machine['id'] == machineId:
        found = True
        print('found machineId %s in machines list' % machine['id'])
if not found:
    print('failed to find machineId %s in machines list' % machineId)
    sys.exit(1)

print("paperspace.machines.stop(...)")
res = paperspace.machines.stop({'machineId': machineId})
errorcheck(res)
paperspace.print_json_pretty(res)

machine = paperspace.machines.waitfor({'machineId': machineId, 'state': 'off'})
errorcheck(machine)
paperspace.print_json_pretty(machine)

print("paperspace.machines.update(...)")
res = paperspace.machines.update({'machineId': machineId, 'machineName': 'pythoncreate-6', 'dynamicPublicIp': False})
errorcheck(res)
paperspace.print_json_pretty(res)

print("paperspace.machines.show(...)")
machine = paperspace.machines.show({'machineId': machineId})
errorcheck(machine)
paperspace.print_json_pretty(machine)

print("paperspace.machines.start(...)")
res = paperspace.machines.start({'machineId': machineId})
errorcheck(res)
paperspace.print_json_pretty(res)

machine = paperspace.machines.waitfor({'machineId': machineId, 'state': 'ready'})
errorcheck(machine)
paperspace.print_json_pretty(machine)

print("paperspace.machines.restart(...)")
res = paperspace.machines.restart({'machineId': machineId})
errorcheck(res)
paperspace.print_json_pretty(res)

time.sleep(10)

machine = paperspace.machines.waitfor({'machineId': machineId, 'state': 'ready'})
errorcheck(machine)
paperspace.print_json_pretty(machine)

print("paperspace.machines.stop(...)")
res = paperspace.machines.stop({'machineId': machineId})
errorcheck(res)
paperspace.print_json_pretty(res)

machine = paperspace.machines.waitfor({'machineId': machineId, 'state': 'off'})
errorcheck(machine)
paperspace.print_json_pretty(machine)

print("paperspace.machines.destroy(...)")
res = paperspace.machines.destroy({'machineId': machineId})
errorcheck(res)
paperspace.print_json_pretty(res)

print("paperspace.machines.utilization(...)")
res = paperspace.machines.utilization({'machineId': machineId, 'billingMonth': '2018-04'})
errorcheck(res)
paperspace.print_json_pretty(res)

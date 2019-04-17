import time

import paperspace
from .method import method


def availability(params):
    return method('machines', 'getAvailability', params)


def create(params):
    return method('machines', 'createSingleMachinePublic', params)


def destroy(params):
    return method('machines', 'destroyMachine', params)


def list(params={}):
    return method('machines', 'getMachines', params)


def restart(params):
    return method('machines', 'restart', params)


def show(params):
    return method('machines', 'getMachinePublic', params)


def start(params):
    return method('machines', 'start', params)


def stop(params):
    return method('machines', 'stop', params)


def waitfor(params):
    params = params.copy()
    if 'machineId' not in params:
        print('Error: machineId is a required parameter for paperspace.machines.waitfor method')
        sys.exit(1)
    if 'state' not in params:
        print('Error: state is a required parameter for paperspace.machines.waitfor method')
        sys.exit(1)
    target_state = params.pop('state', None)
    state = None
    machine = None
    while state != target_state:
        time.sleep(5)
        machine = show(params)
        if 'error' in machine:
            paperspace.print_json_pretty(res)
            sys.exit(1)
        state = machine['state']
    return machine


def update(params):
    return method('machines', 'updateMachinePublic', params)


def utilization(params):
    return method('machines', 'getUtilization', params)

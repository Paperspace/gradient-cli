from .method import method

def list(params={}):
    return method('networks', 'getNetworks', params)

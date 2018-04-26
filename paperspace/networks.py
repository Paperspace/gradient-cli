from .method import *

def list(params={}):
    return method('networks', 'getNetworks', params)

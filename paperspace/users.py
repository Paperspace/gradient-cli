from .method import *

def list(params={}):
    return method('users', 'getUsers', params)

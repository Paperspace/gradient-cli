from .method import method

def list(params={}):
    return method('users', 'getUsers', params)

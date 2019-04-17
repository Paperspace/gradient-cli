from .method import method

def list(params={}):
    return method('templates', 'getTemplates', params)

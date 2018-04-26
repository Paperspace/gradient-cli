from .method import *

def list(params={}):
    return method('templates', 'getTemplates', params)

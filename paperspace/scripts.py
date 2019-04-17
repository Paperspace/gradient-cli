from .method import method

def create(params):
    return method('scripts', 'createScript', params)


def destroy(params):
    return method('scripts', 'destroy', params)


def list(params={}):
    return method('scripts', 'getScripts', params)


def show(params):
    return method('scripts', 'getScript', params)


def text(params):
    return method('scripts', 'getScriptText', params)

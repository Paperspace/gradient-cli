import os

class config: pass

config.PAPERSPACE_API_KEY = ''
config.CONFIG_HOST = 'https://api.paperspace.io'
config.CONFIG_LOG_HOST = 'https://logs.paperspace.io'

if 'PAPERSPACE_API_KEY' in os.environ:
    config.PAPERSPACE_API_KEY = os.environ['PAPERSPACE_API_KEY']

import getpass
import json
import os
import sys

import requests

from . import config


def errorcheck(res, *args):
    if 'error' in res:
        if 'message' in res['error']:
            print(res['error']['message'])
            return False
        print(json.dumps(res, indent=2, sort_keys=True))
        return False
    elif not all(key in res for key in args):
        if 'message' in res:
            print(res['message'])
            return False
        print(json.dumps(res, indent=2, sort_keys=True))
        return False   
    return True


def login(email=None, password=None, apiToken=None):
    paperspace_dir = os.path.expanduser('~/.paperspace')
    config_path = os.path.join(paperspace_dir, 'config.json')
    if not os.path.exists(paperspace_dir):
        os.makedirs(paperspace_dir)
    config_data = {}
    if os.path.exists(config_path):
        config_data = json.load(open(config_path))

    if not email:
        email = input('Email: ')
    if not password:
        password = getpass.getpass('Password: ')

    # get access_token
    params = { "email": email, "password": password }
    r = requests.request('post', config.CONFIG_HOST + '/users/login',
                         json=params)
    res = r.json() 

    if not errorcheck(res, 'id'):
        return False     

    # get api key using access_token
    params = { 'access_token': res['id'] }
    if apiToken:
        params['apiToken'] = apiToken
    r = requests.request('post', config.CONFIG_HOST + '/apiTokens/createPublic',
                         params=params)
    api_token = r.json()
    
    if not errorcheck(api_token, 'key', 'name'):
        return False     

    # update config.PAPERSPACE_API_KEY
    config.PAPERSPACE_API_KEY = api_token['key']

    # save api key
    config_data['apiKey'] = api_token['key']
    config_data['name'] = api_token['name']
    with open(config_path, 'w') as outfile:
        json.dump(config_data, outfile, indent=2, sort_keys=True)
        outfile.write('\n')

    return True


def apikey():
    paperspace_dir = os.path.expanduser('~/.paperspace')
    config_path = os.path.join(paperspace_dir, 'config.json')
    if os.path.exists(config_path):
        config_data = json.load(open(config_path))
        if config_data and 'apiKey' in config_data:
            return config_data['apiKey']
    return ''


def logout():
    paperspace_dir = os.path.expanduser('~/.paperspace')
    config_path = os.path.join(paperspace_dir, 'config.json')
    if os.path.exists(config_path):
        config_data = {}
        with open(config_path, 'w') as outfile:
            json.dump(config_data, outfile, indent=2, sort_keys=True)
            outfile.write('\n')

if __name__ == '__main__':
	email, password, apiToken, *rest = sys.argv[1:] + [None] * 3
	if not login(email, password, apiToken):
		sys.exit(1)

import getpass
import json
import os
import sys

import requests
from six.moves import input

from . import config
from .method import *


def is_error_or_missing_keys_print(res, *required_keys):
    if 'error' in res:
        if 'message' in res:
            print(res['message'])
            return True
        if 'message' in res['error']:
            print(res['error']['message'])
            return True
        print(json.dumps(res, indent=2, sort_keys=True))
        return True
    elif not all(key in res for key in required_keys):
        if 'message' in res:
            print(res['message'])
            return True
        print(json.dumps(res, indent=2, sort_keys=True))
        return True
    return False


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
    try:
        r = requests.request('post', config.CONFIG_HOST + '/users/login',
                             json=params)
    except requests.exceptions.RequestException as e:
        res = requests_exception_to_error_obj(e)
    else:
        try:
            res = response_error_check(r.json())
        except ValueError:
            res = status_code_to_error_obj(r.status_code)

    if is_error_or_missing_keys_print(res, 'id'):
        return False

    # get api key using access_token
    params = { 'access_token': res['id'] }
    if apiToken:
        params['apiToken'] = apiToken
    try:
        r = requests.request('post', config.CONFIG_HOST + '/apiTokens/createPublic',
                             params=params)
    except requests.exceptions.RequestException as e:
        res = requests_exception_to_error_obj(e)
    else:
        try:
            res = response_error_check(r.json())
        except ValueError:
            res = status_code_to_error_obj(r.status_code)

    if is_error_or_missing_keys_print(res, 'key', 'name'):
        return False

    api_token = res

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
    return True

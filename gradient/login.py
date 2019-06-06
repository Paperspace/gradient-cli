import getpass
import json
import os

import requests
from six.moves import input

from gradient import logger
from .config import config
from gradient.utils import response_error_check, requests_exception_to_error_obj, status_code_to_error_obj

UNAUTHORIZED_EXTENDED_INFO = '\n\nNote: Please keep in mind that currently you can login only with the email and ' \
                             'password from your Paperspace account. If you\'re using AD, SAML or GitHub ' \
                             'credentials, please log into the Paperspace Console and create an API key for use with ' \
                             'the CLI client. For more information, please refer to the CLI client documentation.'


def is_error_or_missing_keys_print(res, *required_keys):
    if 'error' in res:
        if 'message' in res:
            print(res['message'])
            return True
        if 'message' in res['error']:
            error_message = res['error']['message'] + UNAUTHORIZED_EXTENDED_INFO
            print(error_message)
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
    params = {"email": email, "password": password}
    try:
        r = requests.request('post', config.CONFIG_HOST + '/users/login',
                             json=params)
        logger.debug(r.content)
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
    params = {'access_token': res['id']}
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


def set_apikey(apikey):
    paperspace_dir = os.path.expanduser('~/.paperspace')
    config_path = os.path.join(paperspace_dir, 'config.json')
    if not os.path.exists(paperspace_dir):
        os.makedirs(paperspace_dir)
    config_data = {}

    # update config.PAPERSPACE_API_KEY
    config.PAPERSPACE_API_KEY = apikey

    # save api key
    config_data['apiKey'] = apikey
    with open(config_path, 'w') as outfile:
        json.dump(config_data, outfile, indent=2, sort_keys=True)
        outfile.write('\n')

    logger.log("Successfully added your API Key to {}. You're ready to go!".format(config_path))

    return True


def logout():
    paperspace_dir = os.path.expanduser('~/.paperspace')
    config_path = os.path.join(paperspace_dir, 'config.json')
    if os.path.exists(config_path):
        config_data = {}
        with open(config_path, 'w') as outfile:
            json.dump(config_data, outfile, indent=2, sort_keys=True)
            outfile.write('\n')
    return True

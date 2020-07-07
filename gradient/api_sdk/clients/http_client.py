import copy

import requests

from gradient import version
from .. import utils, logger as sdk_logger
from ..config import config

default_headers = {"X-API-Key": config.PAPERSPACE_API_KEY,
                   "ps_client_name": "gradient-cli-sdk",
                   "ps_client_version": version.version}


class API(object):
    def __init__(self, api_url, headers=None, api_key=None, ps_client_name=None, logger=sdk_logger.MuteLogger()):
        """

        :param str api_url: url you want to connect
        :param dict headers: headers
        :param str api_key: your API key
        :param str ps_client_name: Client name
        :param sdk_logger.Logger logger:
        """
        self.api_url = api_url
        headers = headers or default_headers
        self.headers = headers.copy()

        if api_key:
            self.api_key = api_key

        if ps_client_name is not None:
            self.ps_client_name = ps_client_name

        self.logger = logger

    @property
    def api_key(self):
        return self.headers.get("X-API-Key")

    @api_key.setter
    def api_key(self, value):
        self.headers["X-API-Key"] = value

    @property
    def ps_client_name(self):
        return self.headers.get("ps_client_name")

    @ps_client_name.setter
    def ps_client_name(self, value):
        self.headers["ps_client_name"] = value

    def get_path(self, url):
        if not url:
            return self.api_url

        full_path = utils.concatenate_urls(self.api_url, url)
        return full_path

    def post(self, url, json=None, params=None, files=None, data=None):
        path = self.get_path(url)
        headers = copy.deepcopy(self.headers)
        if data:
            headers["Content-Type"] = data.content_type

        self.logger.debug("POST request sent to: {} \n\theaders: {}\n\tjson: {}\n\tparams: {}\n\tfiles: {}\n\tdata: {}"
                          .format(path, headers, json, params, files, data))
        response = requests.post(path, json=json, params=params, headers=headers, files=files, data=data)
        self.logger.debug("Response status code: {}".format(response.status_code))
        self.logger.debug("Response content: {}".format(response.content))
        return response

    def put(self, url, json=None, params=None, data=None):
        path = self.get_path(url)
        self.logger.debug("PUT request sent to: {} \n\theaders: {}\n\tjson: {}\n\tparams: {}"
                          .format(path, self.headers, json, params))
        response = requests.put(path, json=json, params=params, headers=self.headers, data=data)
        self.logger.debug("Response status code: {}".format(response.status_code))
        self.logger.debug("Response content: {}".format(response.content))
        return response

    def get(self, url, json=None, params=None):
        path = self.get_path(url)
        self.logger.debug("GET request sent to: {} \n\theaders: {}\n\tjson: {}\n\tparams: {}"
                          .format(path, self.headers, json, params))
        response = requests.get(path, params=params, headers=self.headers, json=json)
        self.logger.debug("Response status code: {}".format(response.status_code))
        self.logger.debug("Response content: {}".format(response.content))
        return response

    def delete(self, url, json=None, params=None):
        path = self.get_path(url)
        response = requests.delete(path, params=params, headers=self.headers, json=json)
        self.logger.debug("DELETE request sent to: {} \n\theaders: {}\n\tjson: {}\n\tparams: {}"
                          .format(response.url, self.headers, json, params))
        self.logger.debug("Response status code: {}".format(response.status_code))
        self.logger.debug("Response content: {}".format(response.content))
        return response


class GradientResponse(object):
    def __init__(self, body, code, headers, data, request=None):
        self.body = body
        self.code = code
        self.headers = headers
        self.data = data
        self.request = request

    @property
    def ok(self):
        return 200 <= self.code < 400

    @classmethod
    def interpret_response(cls, response):
        """
        :type response: requests.Response
        :rtype: GradientResponse
        """
        try:
            data = response.json()
        except ValueError:
            content = response.content
            data = content or None

        gradient_response = cls(response.content, response.status_code, response.headers, data,
                                request=response.request)
        return gradient_response

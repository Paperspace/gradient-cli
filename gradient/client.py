import requests

from gradient import logger, config, version

default_headers = {"X-API-Key": config.PAPERSPACE_API_KEY,
                   "ps_client_name": "paperspace-python",
                   "ps_client_version": version.version}


class API(object):
    def __init__(self, api_url, headers=None, api_key=None, logger_=logger.Logger()):
        self.api_url = api_url
        headers = headers or default_headers
        self.headers = headers.copy()
        if api_key:
            self.api_key = api_key
        self.logger = logger_

    @property
    def api_key(self):
        return self.headers.get("X-API-Key")

    @api_key.setter
    def api_key(self, value):
        self.headers["X-API-Key"] = value

    def get_path(self, url):
        api_url = self.api_url if not self.api_url.endswith("/") else self.api_url[:-1]
        template = "{}{}" if url.startswith("/") else "{}/{}"
        return template.format(api_url, url)

    def post(self, url, json=None, params=None, files=None, data=None):
        path = self.get_path(url)
        self.logger.debug("POST request sent to: {} \n\theaders: {}\n\tjson: {}\n\tparams: {}\n\tfiles: {}\n\tdata: {}"
                     .format(path, self.headers, json, params, files, data))
        response = requests.post(path, json=json, params=params, headers=self.headers, files=files, data=data)
        self.logger.debug("Response status code: {}".format(response.status_code))
        self.logger.debug("Response content: {}".format(response.content))
        return response

    def put(self, url, json=None, params=None):
        path = self.get_path(url)
        self.logger.debug("PUT request sent to: {} \n\theaders: {}\n\tjson: {}\n\tparams: {}"
                     .format(path, self.headers, json, params))
        response = requests.put(path, json=json, params=params, headers=self.headers)
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

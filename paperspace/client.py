import requests

from paperspace import logger, config, version

default_headers = {"X-API-Key": config.PAPERSPACE_API_KEY,
                   "ps_client_name": "paperspace-python",
                   "ps_client_version": version.version}


class API(object):
    def __init__(self, api_url, headers=None):
        self.api_url = api_url
        headers = headers or default_headers
        self.headers = headers.copy()

    def get_path(self, url):
        api_url = self.api_url if not self.api_url.endswith("/") else self.api_url[:-1]
        template = "{}{}" if url.startswith("/") else "{}/{}"
        return template.format(api_url, url)

    def post(self, url, json=None, params=None):
        path = self.get_path(url)
        response = requests.post(path, json=json, params=params, headers=self.headers)
        logger.debug("POST request sent to: {} with headers: {}".format(response.url, self.headers))
        logger.debug("Response status code: {}".format(response.status_code))
        logger.debug("Response content: {}".format(response.content))
        return response

    def put(self, url):
        path = self.get_path(url)
        response = requests.put(path, headers=self.headers)
        logger.debug("PUT request sent to: {} with headers: {}".format(response.url, self.headers))
        logger.debug("Response status code: {}".format(response.status_code))
        logger.debug("Response content: {}".format(response.content))
        return response

    def get(self, url, params=None):
        path = self.get_path(url)
        response = requests.get(path, params=params, headers=self.headers)
        logger.debug("GET request sent to: {} with headers: {}".format(response.url, self.headers))
        logger.debug("Response status code: {}".format(response.status_code))
        logger.debug("Response content: {}".format(response.content))
        return response

    @property
    def api_key(self):
        return self.headers.get("X-API-Key")

    @api_key.setter
    def api_key(self, value):
        self.headers["X-API-Key"] = value

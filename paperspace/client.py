import requests


class API(object):
    def __init__(self, api_url, headers=None):
        self.api_url = api_url
        self.headers = headers or {}

    def get_path(self, url):
        template = "{}{}" if url.startswith("/") else "{}/{}"
        return template.format(self.api_url, url)

    def post(self, url, json=None):
        path = self.get_path(url)
        response = requests.post(path, json=json, headers=self.headers)
        return response

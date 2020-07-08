class MockResponse:
    def __init__(self, json_data=None, status_code=200, content="", headers=None, request=None):
        """
        :type json_data: dict|list
        :type status_code: int
        """
        self.json_data = json_data
        self.status_code = status_code
        self.content = content
        self.url = "example.com"
        self.headers = headers
        self.request = request

    @property
    def ok(self):
        return 200 <= self.status_code <= 299

    def json(self):
        if self.json_data is None:
            raise ValueError("No JSON")
        return self.json_data

class MockResponse:
    def __init__(self, json_data, status_code, content):
        self.json_data = json_data
        self.status_code = status_code
        self.content = content
        self.url = "example.com"

    @property
    def ok(self):
        return 200 <= self.status_code <= 299

    def json(self):
        if not self.json_data:
            raise ValueError("No data")

        return self.json_data

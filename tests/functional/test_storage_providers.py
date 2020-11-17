import mock
from click.testing import CliRunner

from gradient.api_sdk.clients import http_client
from gradient.cli import cli
from tests import example_responses, MockResponse

EXPECTED_HEADERS = http_client.default_headers.copy()
EXPECTED_HEADERS["ps_client_name"] = "gradient-cli"

EXPECTED_HEADERS_WITH_CHANGED_API_KEY = EXPECTED_HEADERS.copy()
EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"

URL = "https://api.paperspace.io"


class TestListStorageProviders(object):
    COMMAND = ["storageProviders", "list"]

    JSON = example_responses.LIST_STORAGE_PROVIDERS_RESPONSE

    STDOUT = """+-------+-----------------+------+---------------------------------+
| Name  | ID              | Type | Config                          |
+-------+-----------------+------+---------------------------------+
| test1 | spltautet072md4 | s3   | accessKey: AKIBAEG7J3OJ24XAV33B |
|       |                 |      | bucket: bucket                  |
|       |                 |      | secretAccessKey: ********       |
+-------+-----------------+------+---------------------------------+
"""

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_list_storage_providers(self, method):
        method.return_value = MockResponse(self.JSON)

        result = CliRunner().invoke(cli.cli, self.COMMAND)

        assert self.STDOUT == result.output, result.exc_info
        method.assert_called_once_with(
            URL + "/storageProviders",
            headers=EXPECTED_HEADERS,
            json=None,
            params={
                "filter[limit]": 21,
                "filter[skip]": 0,
                "filter[order][]": "name ASC",
            }
        )


class TestShowStorageProviderDetails(object):
    COMMAND = ["storageProviders", "details"]

    JSON = example_responses.SHOW_STORAGE_PROVIDER_DETAILS_RESPONSE

    STDOUT = """+--------+---------------------------------+
| Name   | test1                           |
+--------+---------------------------------+
| ID     | spltautet072md4                 |
| Type   | s3                              |
| Config | accessKey: AKIBAEG7J3OJ24XAV33B |
|        | bucket: bucket                  |
|        | secretAccessKey: ********       |
+--------+---------------------------------+
"""

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_show_storage_provider_details(self, method):
        method.return_value = MockResponse(self.JSON)

        result = CliRunner().invoke(cli.cli, self.COMMAND + ["--id=spltautet072md4"])

        assert self.STDOUT in result.output, result.exc_info
        method.assert_called_once_with(
            URL + "/storageProviders/spltautet072md4",
            headers=EXPECTED_HEADERS,
            json=None,
            params=None
        )


class TestCreateStorageProvider(object):
    COMMAND = ["storageProviders", "create"]

    JSON = example_responses.CREATE_STORAGE_PROVIDER_RESPONSE

    STDOUT = """Created new storage provider with id: spltautet072md4
"""

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_create_storage_provider(self, method):
        method.return_value = MockResponse(self.JSON)

        result = CliRunner().invoke(cli.cli, self.COMMAND + [
            "s3", "--name=test1", "--bucket=bucket", "--accessKey=AKIBAEG7J3OJ24XAV33B", "--secretAccessKey=bla"])

        assert self.STDOUT in result.output, result.exc_info
        method.assert_called_once_with(
            URL + "/storageProviders",
            json={
                "name": "test1",
                "type": "s3",
                "config": {"bucket": "bucket", "accessKey": "AKIBAEG7J3OJ24XAV33B", "secretAccessKey": "bla"},
            },
            params=None,
            headers=EXPECTED_HEADERS,
            files=None,
            data=None
        )


class TestUpdateStorageProvider(object):
    COMMAND = ["storageProviders", "update"]

    JSON = example_responses.UPDATE_STORAGE_PROVIDER_RESPONSE

    STDOUT = """Updated storage provider
"""

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_update_storage_provider(self, method):
        method.return_value = MockResponse(self.JSON)

        result = CliRunner().invoke(cli.cli, self.COMMAND + ["s3", "--id=spltautet072md4", "--name=test2"])

        assert self.STDOUT in result.output, result.exc_info
        method.assert_called_once_with(
            URL + "/storageProviders/spltautet072md4",
            json={"name": "test2"},
            params=None,
            headers=EXPECTED_HEADERS,
            files=None,
            data=None
        )


class TestDeleteStorageProvider(object):
    COMMAND = ["storageProviders", "delete"]

    STDOUT = """Deleted storage provider: spltautet072md4
"""

    @mock.patch("gradient.api_sdk.clients.http_client.requests.delete")
    def test_delete_storage_provider(self, method):
        method.return_value = MockResponse(status_code=204)

        result = CliRunner().invoke(cli.cli, self.COMMAND + ["--id=spltautet072md4"])

        assert self.STDOUT in result.output, result.exc_info
        method.assert_called_once_with(
            URL + "/storageProviders/spltautet072md4",
            params=None,
            headers=EXPECTED_HEADERS,
            json=None
        )

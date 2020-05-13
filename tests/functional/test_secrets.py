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


class TestSecretsList(object):
    COMMAND = ["secrets", "list"]

    LIST_SECRETS = example_responses.LIST_SECRETS_RESPONSE

    LIST_STDOUT = """+-----------------------+
| Name                  |
+-----------------------+
| aws_access_key_id     |
| aws_secret_access_key |
+-----------------------+
"""

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_list_of_secrets(self, get_patched):
        get_patched.return_value = MockResponse(self.LIST_SECRETS)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND + ["team"])

        assert self.LIST_STDOUT in result.output, result.exc_info
        get_patched.assert_called_once_with(URL + "/teams/secrets",
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params={})

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_list_of_secrets_with_id(self, get_patched):
        get_patched.return_value = MockResponse(self.LIST_SECRETS)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND + ["team", "--id", "te1234567"])

        assert self.LIST_STDOUT in result.output, result.exc_info
        get_patched.assert_called_once_with(URL + "/teams/secrets",
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params={"teamId": "te1234567"})


class TestSecretsSet(object):
    COMMAND = ["secrets", "set"]

    SET_STDOUT = "Set {} secret 'aws_access_key_id'\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    def test_should_send_put_request_and_print_status(self, put_patched):
        put_patched.return_value = MockResponse()

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND + ["team", "--name=aws_access_key_id", "--value=secret"])

        assert self.SET_STDOUT.format("team") in result.output, result.exc_info
        put_patched.assert_called_once_with(URL + "/teams/secrets/aws_access_key_id",
                                            headers=EXPECTED_HEADERS,
                                            params={},
                                            json={"value": "secret"},
                                            data=None)


    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    def test_should_send_put_request_and_print_status_with_id(self, put_patched):
        put_patched.return_value = MockResponse()

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND + ["project", "--id=pr1234567",
                                                        "--name=aws_access_key_id", "--value=secret"])

        assert self.SET_STDOUT.format("project") in result.output, result.exc_info
        put_patched.assert_called_once_with(URL + "/projects/secrets/aws_access_key_id",
                                            headers=EXPECTED_HEADERS,
                                            params={"projectId": "pr1234567"},
                                            json={"value": "secret"},
                                            data=None)


class TestSecretsDelete(object):
    COMMAND = ["secrets", "delete"]

    SET_STDOUT = "Deleted cluster secret 'aws_secret_access_key'\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.delete")
    def test_should_send_delete_request_and_print_status_with_id(self, delete_patched):
        delete_patched.return_value = MockResponse()

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND + ["team", "--name=aws_secret_access_key"])

        assert self.SET_STDOUT in result.output, result.exc_info
        delete_patched.assert_called_once_with(URL + "/teams/secrets/aws_secret_access_key",
                                               headers=EXPECTED_HEADERS,
                                               params={},
                                               json=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.delete")
    def test_should_send_delete_request_and_print_status_with_id(self, delete_patched):
        delete_patched.return_value = MockResponse()

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND + ["cluster", "--id=cl1234567",
                                                        "--name=aws_secret_access_key"])

        assert self.SET_STDOUT in result.output, result.exc_info
        delete_patched.assert_called_once_with(URL + "/clusters/secrets/aws_secret_access_key",
                                               headers=EXPECTED_HEADERS,
                                               params={"clusterId": "cl1234567"},
                                               json=None)

import mock
from click.testing import CliRunner

from gradient.api_sdk.clients import http_client
from gradient.cli import cli
from tests import example_responses, MockResponse


class TestClustersList(object):
    URL = "https://api.paperspace.io/clusters/getClusters"

    COMMAND = ["clusters", "list"]
    COMMAND_WITH_LIMIT = COMMAND[:] + ["-l", "2"]
    COMMAND_WITH_OPTIONS_FILE = ["clusters", "list", "--optionsFile", ]  # path added in test

    LIST_CLUSTERS = example_responses.EXAMPLE_CLUSTERS_LIST_RESPONSE
    LIMITED_LIST_CLUSTERS = example_responses.LIMITED_EXAMPLE_CLUSTERS_LIST_RESPONSE

    DEFAULT_PARAMS = {
        "filter": '{"limit": 20, "offset": 0, "where": {"isPrivate": true}}'
    }
    LIMITED_PARAMS = {
        "filter": '{"limit": 2, "offset": 0, "where": {"isPrivate": true}}'
    }

    COMMAND_WITH_API_KEY = ["clusters", "list", "--apiKey", "some_key"]
    EXPECTED_HEADERS = http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"

    LIST_STDOUT = """+--------------+----------------+----------------------------+
| ID           | Name           | Type                       |
+--------------+----------------+----------------------------+
| cluster_id_1 | cluster name 1 | Job Cluster                |
| cluster_id_2 | cluster name 2 | Kubernetes Processing Site |
| cluster_id_3 | cluster name 3 | Job Cluster                |
+--------------+----------------+----------------------------+
"""
    PAGINATED_LIST_STDOUT = """+--------------+----------------+----------------------------+
| ID           | Name           | Type                       |
+--------------+----------------+----------------------------+
| cluster_id_1 | cluster name 1 | Job Cluster                |
| cluster_id_2 | cluster name 2 | Kubernetes Processing Site |
+--------------+----------------+----------------------------+

Do you want to continue? [y/N]: 
Aborted!
"""

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_list_of_clusters(self, get_patched):
        get_patched.return_value = MockResponse(self.LIST_CLUSTERS, 200, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert self.LIST_STDOUT in result.output, result.exc_info
        get_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS,
                                            json=None,
                                            params=self.DEFAULT_PARAMS)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_paginate_list_of_clusters(self, get_patched):
        get_patched.return_value = MockResponse(self.LIMITED_LIST_CLUSTERS, 200, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_LIMIT)

        assert self.PAGINATED_LIST_STDOUT in str(result.output)
        get_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS,
                                            json=None,
                                            params=self.LIMITED_PARAMS)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_options_defined_in_a_config_file(self, get_patched, clusters_list_config_path):
        get_patched.return_value = MockResponse(json_data=self.LIMITED_LIST_CLUSTERS,
                                                status_code=200)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [clusters_list_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert self.PAGINATED_LIST_STDOUT in str(result.output)
        get_patched.assert_called_once_with(self.URL,
                                            headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                            json=None,
                                            params=self.LIMITED_PARAMS,
                                            )

import mock
from click.testing import CliRunner

from gradient.api_sdk.clients import http_client
from gradient.cli import cli
from tests import example_responses, MockResponse

EXPECTED_HEADERS = http_client.default_headers.copy()
EXPECTED_HEADERS["ps_client_name"] = "gradient-cli"

EXPECTED_HEADERS_WITH_CHANGED_API_KEY = EXPECTED_HEADERS.copy()
EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"


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
        get_patched.return_value = MockResponse(self.LIST_CLUSTERS)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert self.LIST_STDOUT in result.output, result.exc_info
        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params=self.DEFAULT_PARAMS)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_paginate_list_of_clusters(self, get_patched):
        get_patched.return_value = MockResponse(self.LIMITED_LIST_CLUSTERS)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_LIMIT)

        assert self.PAGINATED_LIST_STDOUT in str(result.output)
        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params=self.LIMITED_PARAMS)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_options_defined_in_a_config_file(self, get_patched, clusters_list_config_path):
        get_patched.return_value = MockResponse(json_data=self.LIMITED_LIST_CLUSTERS)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [clusters_list_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert self.PAGINATED_LIST_STDOUT in str(result.output)
        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                            json=None,
                                            params=self.LIMITED_PARAMS,
                                            )


class TestListVmTypes(object):
    URL = "https://api.paperspace.io/vmTypes/getVmTypesByClusters"

    COMMAND = ["clusters", "machineTypes", "list"]
    COMMAND_WITH_FILTERING_BY_CLUSTER_ID = ["clusters", "machineTypes", "list", "--clusterId", "cluwffvkb"]
    COMMAND_WITH_FILTERING_BY_INVALID_ID = ["clusters", "machineTypes", "list", "--clusterId", "invalid_id"]
    COMMAND_WITH_OPTIONS_FILE = ["clusters", "machineTypes", "list", "--optionsFile", ]  # path added in test

    LIST_JSON = example_responses.LIST_OF_VM_MACHINE_TYPES
    EXPECTED_STDOUT = """+--------------+---------+-----------+--------------+-----------+------------+---------------------------------+
| Name         | Kind    | CPU Count | RAM [Bytes]  | GPU Count | GPU Model  | Clusters                        |
+--------------+---------+-----------+--------------+-----------+------------+---------------------------------+
| Wolfpass-CPU | cpu     | 24        | 34359738368  | 1         | N/A        | clfe0kr2p                       |
| c5.24xlarge  | aws-cpu | 94        | 206158430208 | 1         | N/A        | cluwffvkb                       |
| c5.4xlarge   | aws-cpu | 16        | 34359738368  | 1         | N/A        | clqr4b0ox, clrvkwq6l, cluwffvkb |
| c5.xlarge    | aws-cpu | 4         | 8589934592   | 1         | N/A        | clqr4b0ox, clrvkwq6l, cluwffvkb |
| p2.xlarge    | aws-gpu | 4         | 65498251264  | 1         | Tesla K80  | clqr4b0ox, clrvkwq6l            |
| p3.16xlarge  | aws-gpu | 64        | 523986010112 | 8         | Tesla V100 | clqr4b0ox, clrvkwq6l, cluwffvkb |
| p3.2xlarge   | aws-gpu | 8         | 65498251264  | 1         | Tesla V100 | clqr4b0ox, clrvkwq6l, cluwffvkb |
+--------------+---------+-----------+--------------+-----------+------------+---------------------------------+
"""

    DETAILS_STDOUT_WITH_FILTERING_BY_CLUSTER_ID = """+-------------+---------+-----------+--------------+-----------+------------+---------------------------------+
| Name        | Kind    | CPU Count | RAM [Bytes]  | GPU Count | GPU Model  | Clusters                        |
+-------------+---------+-----------+--------------+-----------+------------+---------------------------------+
| c5.24xlarge | aws-cpu | 94        | 206158430208 | 1         | N/A        | cluwffvkb                       |
| c5.4xlarge  | aws-cpu | 16        | 34359738368  | 1         | N/A        | clqr4b0ox, clrvkwq6l, cluwffvkb |
| c5.xlarge   | aws-cpu | 4         | 8589934592   | 1         | N/A        | clqr4b0ox, clrvkwq6l, cluwffvkb |
| p3.16xlarge | aws-gpu | 64        | 523986010112 | 8         | Tesla V100 | clqr4b0ox, clrvkwq6l, cluwffvkb |
| p3.2xlarge  | aws-gpu | 8         | 65498251264  | 1         | Tesla V100 | clqr4b0ox, clrvkwq6l, cluwffvkb |
+-------------+---------+-----------+--------------+-----------+------------+---------------------------------+
"""

    RESPONSE_JSON_WHEN_WRONG_API_KEY_WAS_USED = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WHEN_WRONG_API_KEY_WAS_USED = "Failed to fetch data: Invalid API token\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_list_of_machine_types(self, get_patched):
        get_patched.return_value = MockResponse(self.LIST_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT
        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params=None)

        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_list_of_vm_machine_types_filtered_by_cluster_id(self, get_patched):
        get_patched.return_value = MockResponse(self.LIST_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_FILTERING_BY_CLUSTER_ID)

        assert result.output == self.DETAILS_STDOUT_WITH_FILTERING_BY_CLUSTER_ID, result.exc_info
        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params=None)

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_list_of_machine_types_but_none_found(self, get_patched):
        get_patched.return_value = MockResponse(self.LIST_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_FILTERING_BY_INVALID_ID)

        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params=None)

        assert result.output == "No data found\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_proper_message_when_wrong_api_key_was_used(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WHEN_WRONG_API_KEY_WAS_USED,
                                                status_code=403)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS,
                                            json=None,
                                            params=None)

        assert result.output == self.EXPECTED_STDOUT_WHEN_WRONG_API_KEY_WAS_USED
        assert EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_options_defined_in_a_config_file(self, get_patched, vm_machine_types_list_config_path):
        get_patched.return_value = MockResponse(self.LIST_JSON)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [vm_machine_types_list_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == self.DETAILS_STDOUT_WITH_FILTERING_BY_CLUSTER_ID
        get_patched.assert_called_once_with(self.URL,
                                            headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                            json=None,
                                            params=None)

import mock
from click.testing import CliRunner

from gradient.api_sdk.clients.http_client import default_headers
from gradient.cli import cli
from tests import MockResponse, example_responses

EXPECTED_HEADERS = default_headers.copy()
EXPECTED_HEADERS["ps_client_name"] = "gradient-cli"

EXPECTED_HEADERS_WITH_CHANGED_API_KEY = EXPECTED_HEADERS.copy()
EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"


class TestMachineAvailability(object):
    URL = "https://api.paperspace.io/machines/getAvailability/"
    COMMAND = [
        "machines", "availability",
        "--region", "ny2",
        "--machineType", "P4000",
    ]
    PARAMS = {"region": "East Coast (NY2)", "machineType": "P4000"}
    RESPONSE_JSON = {"available": True}

    COMMAND_WITH_API_KEY = [
        "machines", "availability",
        "--region", "ny2",
        "--machineType", "P4000",
        "--apiKey", "some_key",
    ]
    COMMAND_WITH_OPTIONS_FILE = ["machines", "availability", "--optionsFile", ]  # path added in test

    EXPECTED_STDOUT = "Machine available: True\n"

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Failed to fetch data: Invalid API token\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_get_request_and_print_valid_message_when_availability_command_was_used(self, get_patched):
        get_patched.return_value = MockResponse(self.RESPONSE_JSON, 200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=None,
                                       params=self.PARAMS)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_changed_headers_when_api_key_option_was_used(self, get_patched):
        get_patched.return_value = MockResponse(self.RESPONSE_JSON, 200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.PARAMS)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_options_from_yaml_file(self, get_patched, machines_availability_config_path):
        get_patched.return_value = MockResponse(self.RESPONSE_JSON)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [machines_availability_config_path]

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, command)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.PARAMS)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_valid_error_message_when_availability_command_was_used_with_invalid_api_token(self,
                                                                                                        get_patched):
        get_patched.return_value = MockResponse(self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, 400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=None,
                                       params=self.PARAMS)
        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_valid_error_message_when_no_content_was_received_in_response(self, get_patched):
        get_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=None,
                                       params=self.PARAMS)
        assert result.output == "Unknown error while checking machine availability\n"
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_valid_error_message_when_no_content_was_received_in_response(self, get_patched):
        get_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=None,
                                       params=self.PARAMS)
        assert result.output == "Failed to fetch data\n"
        assert result.exit_code == 0


class TestCreateMachine(object):
    URL = "https://api.paperspace.io/machines/createSingleMachinePublic/"
    TAGS_URL = "https://api.paperspace.io/entityTags/updateTags"
    BASIC_COMMAND = [
        "machines", "create",
        "--region", "CA1",
        "--machineType", "P5000",
        "--size", 2,
        "--billingType", "hourly",
        "--machineName", "some_name",
        "--templateId", "some_template",
    ]
    BASIC_COMMAND_WITH_TAGS = [
        "machines", "create",
        "--region", "CA1",
        "--machineType", "P5000",
        "--size", 2,
        "--billingType", "hourly",
        "--machineName", "some_name",
        "--templateId", "some_template",
        "--tag", "test0",
        "--tag", "test1",
        "--tags", "test2,test3",
    ]
    REQUEST_JSON = {
        "billingType": "hourly",
        "machineType": "P5000",
        "machineName": "some_name",
        "region": "West Coast (CA1)",
        "templateId": "some_template",
        "size": 2,
    }
    TAGS_JSON = {
        "entity": "machine",
        "entityId": "psclbvqpc",
        "tags": ["test0", "test1", "test2", "test3"]
    }

    ALL_COMMANDS = [
        "machines", "create",
        "--apiKey", "some_key",
        "--assignPublicIp",
        "--billingType", "hourly",
        "--email", "some@ema.il",
        "--firstName", "some_f_name",
        "--lastName", "some_l_name",
        "--machineName", "some_name",
        "--machineType", "P5000",
        "--networkId", "some_network_id",
        "--notificationEmail", "some@em.a.il",
        "--password", "some_password",
        "--region", "CA1",
        "--scriptId", "some_script_id",
        "--size", "2",
        "--teamId", "some_team_id",
        "--templateId", "some_template",
    ]
    ALL_OPTIONS_REQUEST_JSON = {
        "assignPublicIp": True,
        "billingType": "hourly",
        "email": "some@ema.il",
        "firstName": "some_f_name",
        "lastName": "some_l_name",
        "machineName": "some_name",
        "machineType": "P5000",
        "networkId": "some_network_id",
        "notificationEmail": "some@em.a.il",
        "password": "some_password",
        "region": "West Coast (CA1)",
        "scriptId": "some_script_id",
        "size": 2,
        "teamId": "some_team_id",
        "templateId": "some_template",
    }

    BASIC_COMMAND_WITH_API_KEY = [
        "machines", "create",
        "--region", "CA1",
        "--machineType", "P5000",
        "--size", 2,
        "--billingType", "hourly",
        "--machineName", "some_name",
        "--templateId", "some_template",
        "--apiKey", "some_key",
    ]

    COMMAND_WITH_OPTIONS_FILE = ["machines", "create", "--optionsFile", ]  # path added in test

    EXPECTED_STDOUT = "New machine created with id: psclbvqpc\n" \
                      "https://console.paperspace.com/machines/psclbvqpc\n"

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Failed to create resource: Invalid API token\n"
    UPDATE_TAGS_RESPONSE_JSON_200 = example_responses.UPDATE_TAGS_RESPONSE

    RESPONSE_JSON_WITH_WRONG_TEMPLATE_ID = {
        "error": {
            "name": "Error",
            "status": 400,
            "message": "templateId not found"
        }
    }

    BASIC_COMMAND_WITH_MUTUALLY_EXCLUSIVE_OPTIONS_USED = [
        "machines", "create",
        "--region", "CA1",
        "--machineType", "P5000",
        "--size", 2,
        "--billingType", "hourly",
        "--machineName", "some_name",
        "--templateId", "some_template",
        "--userId", "some_user_id",
        "--email", "some@email.com",
    ]

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_valid_post_request_when_machine_create_was_used_with_requested_options(self, get_patched):
        get_patched.return_value = MockResponse(example_responses.CREATE_MACHINE_RESPONSE, 200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=self.REQUEST_JSON,
                                       params=None,
                                       files=None,
                                       data=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_valid_post_request_when_machine_create_was_used_with_all_options(self, post_patched):
        post_patched.return_value = MockResponse(example_responses.CREATE_MACHINE_RESPONSE, 200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.ALL_COMMANDS)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                        json=self.ALL_OPTIONS_REQUEST_JSON,
                                        params=None,
                                        files=None,
                                        data=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_changed_headers_when_api_key_option_was_used(self, post_patched):
        post_patched.return_value = MockResponse(example_responses.CREATE_MACHINE_RESPONSE, 200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                        json=self.REQUEST_JSON,
                                        params=None,
                                        files=None,
                                        data=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_options_from_yaml_file(self, post_patched, machines_create_config_path):
        post_patched.return_value = MockResponse(example_responses.CREATE_MACHINE_RESPONSE)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [machines_create_config_path]

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, command)

        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                        json=self.ALL_OPTIONS_REQUEST_JSON,
                                        params=None,
                                        files=None,
                                        data=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_error_message_when_wrong_api_key_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, 400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS,
                                        json=self.REQUEST_JSON,
                                        params=None,
                                        files=None,
                                        data=None)
        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_error_message_when_wrong_template_id_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_WITH_WRONG_TEMPLATE_ID, 400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS,
                                        json=self.REQUEST_JSON,
                                        params=None,
                                        files=None,
                                        data=None)
        assert result.output == "Failed to create resource: templateId not found\n"
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_error_message_when_no_content_was_received_in_response(self, post_patched):
        post_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS,
                                        json=self.REQUEST_JSON,
                                        params=None,
                                        files=None,
                                        data=None)
        assert result.output == "Failed to create resource\n"
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_error_message_when_mutually_exclusive_options_were_used(self, get_patched):
        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_MUTUALLY_EXCLUSIVE_OPTIONS_USED)

        get_patched.assert_not_called()
        assert "Error: --userId is mutually exclusive with --email, --password, --firstName and --lastName\n" \
               in result.output
        assert result.exit_code == 2

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_proper_data_and_tag_machine(self, post_patched, get_patched, put_patched):
        post_patched.return_value = MockResponse(example_responses.CREATE_MACHINE_RESPONSE, 200)
        get_patched.return_value = MockResponse({}, 200)
        put_patched.return_value = MockResponse(self.UPDATE_TAGS_RESPONSE_JSON_200, 200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_TAGS)

        post_patched.assert_called_once_with(self.URL,
                                             headers=EXPECTED_HEADERS,
                                             json=self.REQUEST_JSON,
                                             params=None,
                                             files=None,
                                             data=None)

        put_patched.assert_called_once_with(
            self.TAGS_URL,
            headers=EXPECTED_HEADERS,
            json=self.TAGS_JSON,
            params=None,
            data=None,
        )

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        assert result.exit_code == 0


class TestDestroyMachine(object):
    URL = "https://api.paperspace.io/machines/some_id/destroyMachine/"
    BASIC_COMMAND = [
        "machines", "destroy",
        "--id", "some_id",
    ]

    ALL_COMMANDS = [
        "machines", "destroy",
        "--id", "some_id",
        "--releasePublicIp",
    ]
    ALL_COMMANDS_REQUEST_JSON = {"releasePublicIp": True}

    BASIC_COMMAND_WITH_API_KEY = [
        "machines", "destroy",
        "--id", "some_id",
        "--apiKey", "some_key",
    ]

    COMMAND_WITH_OPTIONS_FILE = ["machines", "destroy", "--optionsFile", ]  # path added in test

    EXPECTED_STDOUT = "Machine successfully destroyed\n"

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Failed to delete resource: Invalid API token\n"

    RESPONSE_JSON_WITH_404_MACHINE_NOT_FOUND = {
        "error": {
            "name": "Error",
            "status": 404,
            "message": "Not found. Please contact support@paperspace.com for help."
        }
    }
    EXPECTED_STDOUT_WHEN_MACHINE_WAS_NOT_FOUND = "Failed to delete resource: Not found. " \
                                                 "Please contact support@paperspace.com for help.\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_valid_post_request_when_machines_destroy_was_used(self, post_patched):
        post_patched.return_value = MockResponse(status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS,
                                        json=None,
                                        params=None,
                                        files=None,
                                        data=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_valid_post_request_when_machines_destroy_was_used_with_all_options(self, post_patched):
        post_patched.return_value = MockResponse(status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.ALL_COMMANDS)

        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS,
                                        json=self.ALL_COMMANDS_REQUEST_JSON,
                                        params=None,
                                        files=None,
                                        data=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_options_from_yaml_file(self, post_patched, machines_destroy_config_path):
        post_patched.return_value = MockResponse()
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [machines_destroy_config_path]

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                        json=self.ALL_COMMANDS_REQUEST_JSON,
                                        params=None,
                                        files=None,
                                        data=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_valid_post_request_when_machines_destroy_was_used_with_api_key_option(self, post_patched):
        post_patched.return_value = MockResponse(status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                        json=None,
                                        params=None,
                                        files=None,
                                        data=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_valid_post_request_when_machines_destroy_was_used_with_wrong_api_key(self, post_patched):
        post_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS,
                                        json=None,
                                        params=None,
                                        files=None,
                                        data=None)
        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_error_message_when_machine_with_given_id_was_not_found(self, post_patched):
        post_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WITH_404_MACHINE_NOT_FOUND,
                                                 status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS,
                                        json=None,
                                        params=None,
                                        files=None,
                                        data=None)
        assert result.output == self.EXPECTED_STDOUT_WHEN_MACHINE_WAS_NOT_FOUND
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_error_message_when_error_status_code_received_but_no_content_was_provided(self, post_patched):
        post_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS,
                                        json=None,
                                        params=None,
                                        files=None,
                                        data=None)
        assert result.output == "Failed to delete resource\n"
        assert result.exit_code == 0


class TestListMachines(object):
    URL = "https://api.paperspace.io/machines/getMachines/"
    BASIC_COMMAND = ["machines", "list"]
    REQUEST_JSON = {}
    EXPECTED_RESPONSE_JSON = example_responses.LIST_MACHINES_RESPONSE
    EXPECTED_STDOUT = """+-----------+---------------+------------------------------------------------------------------------------------+-----+------+-----------+--------------+------------------+
| ID        | Name          | OS                                                                                 | CPU | GPU  | RAM       | State        | Region           |
+-----------+---------------+------------------------------------------------------------------------------------+-----+------+-----------+--------------+------------------+
| psclbvqpc | keton2        | None                                                                               | 1   | None | None      | provisioning | None             |
| psbtuwfvt | New Machine 1 | Ubuntu 18.04.1 LTS; uname: 4.15.0-38-generic; distro: ubuntu; major: 18; minor: 04 | 1   | None | 536870912 | off          | East Coast (NY2) |
+-----------+---------------+------------------------------------------------------------------------------------+-----+------+-----------+--------------+------------------+
"""

    COMMAND_WITH_ALL_OPTIONS = [
        "machines", "list",
        "--agentType", "some_agent_type",
        "--apiKey", "some_key",
        "--autoSnapshotFrequency", "hour",
        "--autoSnapshotSaveCount", "2",
        "--cpus", "8",
        "--dtCreated", "2017-09-23T05:55:00.000Z",
        "--dtLastRun", "2017-09-23T05:55:00.000Z",
        "--gpu", "some_gpu",
        "--id", "some_id",
        "--name", "some_name",
        "--networkId", "some_network_id",
        "--os", "some_os",
        "--performAutoSnapshot", "true",
        "--privateIpAddress", "1.2.3.4",
        "--publicIpAddress", "4.3.2.1",
        "--ram", "123",
        "--region", "CA1",
        "--shutdownTimeoutInHours", "3",
        "--state", "some_state",
        "--storageTotal", "123TB",
        "--storageUsed", "123GB",
        "--teamId", "some_team_id",
        "--updatesPending", "True",
        "--usageRate", "some_usage_rate",
        "--userId", "some_user_id",
    ]
    ALL_OPTIONS_REQUEST_JSON = {
        "params": {
            "agentType": "some_agent_type",
            "autoSnapshotFrequency": "hour",
            "autoSnapshotSaveCount": 2,
            "cpus": 8,
            "dtCreated": "2017-09-23T05:55:00.000Z",
            "dtLastRun": "2017-09-23T05:55:00.000Z",
            "gpu": "some_gpu",
            "machineId": "some_id",
            "name": "some_name",
            "networkId": "some_network_id",
            "os": "some_os",
            "performAutoSnapshot": True,
            "privateIpAddress": "1.2.3.4",
            "publicIpAddress": "4.3.2.1",
            "ram": 123,
            "region": "West Coast (CA1)",
            "shutdownTimeoutInHours": 3,
            "state": "some_state",
            "storageTotal": "123TB",
            "storageUsed": "123GB",
            "teamId": "some_team_id",
            "updatesPending": True,
            "usageRate": "some_usage_rate",
            "userId": "some_user_id",
        }
    }

    COMMAND_WITH_PARAMS_OPTION = ["machines", "list",
                                  "--params", '{"cpus":2,"gpu":"ATIRage128"}']
    REQUEST_JSON_WITH_PARAMS_OPTION = {
        "params": {
            "cpus": 2,
            "gpu": "ATIRage128",
        },
    }

    COMMAND_WITH_OPTIONS_FILE = ["machines", "list", "--optionsFile", ]  # path added in test

    BASIC_COMMAND_WITH_API_KEY = ["machines", "list", "--apiKey", "some_key"]

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Failed to fetch data: Invalid API token\n"

    EXPECTED_STDOUT_WHEN_NO_MACHINES_WERE_FOUND = "No data found\n"

    COMMAND_WITH_MUTUALLY_EXCLUSIVE_OPTIONS = [
        "machines", "list",
        "--params", '{"cpus":2,"gpu":"ATIRage128"}',
        "--name", "some_name",
    ]

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_post_request_and_print_table_when_machines_list_was_used(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON, status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=None,
                                       params=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_post_request_when_all_options_were_used(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND_WITH_ALL_OPTIONS)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=self.ALL_OPTIONS_REQUEST_JSON,
                                       params=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_post_request_when_all_options_were_used(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND_WITH_ALL_OPTIONS)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=self.ALL_OPTIONS_REQUEST_JSON,
                                       params=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_post_request_when_params_option_was_used(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON, status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND_WITH_PARAMS_OPTION)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=self.REQUEST_JSON_WITH_PARAMS_OPTION,
                                       params=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_post_request_when_machines_list_was_used_with_api_key_option(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON, status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_options_from_yaml_file(self, get_patched, machines_list_config_path):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [machines_list_config_path]

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, command)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=self.ALL_OPTIONS_REQUEST_JSON,
                                       params=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_post_request_when_machines_list_was_used_with_wrong_api_key(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=None)
        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_error_message_when_no_machine_was_not_found(self, get_patched):
        get_patched.return_value = MockResponse(json_data=[], status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=None,
                                       params=None)
        assert result.output == self.EXPECTED_STDOUT_WHEN_NO_MACHINES_WERE_FOUND
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_error_message_when_error_status_code_received_but_no_content_was_provided(self, get_patched):
        get_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=None,
                                       params=None)
        assert result.output == "Failed to fetch data\n"
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_error_message_when_params_option_was_used_with_mutually_exclusive_option(self, get_patched):
        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND_WITH_MUTUALLY_EXCLUSIVE_OPTIONS)

        get_patched.assert_not_called()
        assert "You can use either --params dictionary or single filter arguments" in result.output
        assert result.exit_code == 2


class TestRestartMachine(object):
    URL = "https://api.paperspace.io/machines/some_id/restart/"
    COMMAND = [
        "machines", "restart",
        "--id", "some_id",
    ]
    EXPECTED_STDOUT = "Machine restarted\n"

    COMMAND_WITH_API_KEY = [
        "machines", "restart",
        "--id", "some_id",
        "--apiKey", "some_key",
    ]

    COMMAND_WITH_OPTIONS_FILE = ["machines", "restart", "--optionsFile", ]  # path added in test

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Unable to restart instance: Invalid API token\n"

    RESPONSE_JSON_WITH_404_MACHINE_NOT_FOUND = {
        "error": {
            "name": "Error",
            "status": 404,
            "message": "Not found. Please contact support@paperspace.com for help."
        }
    }
    EXPECTED_STDOUT_WHEN_MACHINE_WAS_NOT_FOUND = "Unable to restart instance: Not found. " \
                                                 "Please contact support@paperspace.com for help.\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_get_request_and_print_valid_message_when_restart_command_was_used(self, post_patched):
        post_patched.return_value = MockResponse(status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS,
                                        json=None,
                                        params=None,
                                        files=None,
                                        data=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_changed_headers_when_api_key_option_was_used(self, post_patched):
        post_patched.return_value = MockResponse(status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY)

        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                        json=None,
                                        params=None,
                                        files=None,
                                        data=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_options_from_config_file(self, post_patched, machines_restart_config_path):
        post_patched.return_value = MockResponse()
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [machines_restart_config_path]

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                        json=None,
                                        params=None,
                                        files=None,
                                        data=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_valid_error_message_when_start_command_was_used_with_invalid_api_token(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS,
                                        json=None,
                                        params=None,
                                        files=None,
                                        data=None)
        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_valid_error_message_when_no_content_was_received_in_response(self, post_patched):
        post_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS,
                                        json=None,
                                        params=None,
                                        files=None,
                                        data=None)
        assert result.output == "Unable to restart instance\n"
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_error_message_when_machine_with_given_id_was_not_found(self, post_patched):
        post_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WITH_404_MACHINE_NOT_FOUND,
                                                 status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS,
                                        json=None,
                                        params=None,
                                        files=None,
                                        data=None)
        assert result.output == self.EXPECTED_STDOUT_WHEN_MACHINE_WAS_NOT_FOUND
        assert result.exit_code == 0


class TestShowMachine(object):
    URL = "https://api.paperspace.io/machines/getMachinePublic/"
    BASIC_COMMAND = ["machines", "details", "--id", "some_id"]
    REQUEST_PARAMS = {"machineId": "some_id"}
    EXPECTED_RESPONSE_JSON = example_responses.SHOW_MACHINE_RESPONSE
    EXPECTED_STDOUT = """+---------------------------+------------------------------------------------------------------------------------+
| ID                        | some_id                                                                            |
+---------------------------+------------------------------------------------------------------------------------+
| Name                      | New Machine 1                                                                      |
| OS                        | Ubuntu 18.04.1 LTS; uname: 4.15.0-38-generic; distro: ubuntu; major: 18; minor: 04 |
| RAM                       | 536870912                                                                          |
| CPU                       | 1                                                                                  |
| GPU                       | None                                                                               |
| Storage Total             | 53687091200                                                                        |
| Storage Used              | 110080                                                                             |
| Usage Rate                | C1 Hourly                                                                          |
| Shutdown Timeout In Hours | 1                                                                                  |
| Shutdown Timeout Forces   | False                                                                              |
| Perform Auto Snapshot     | True                                                                               |
| Auto snapshot frequency   | month                                                                              |
| Auto Snapshot Save Count  | 1                                                                                  |
| Agent Type                | LinuxHeadless                                                                      |
| Created                   | 2019-04-11T18:10:29.665Z                                                           |
| State                     | off                                                                                |
| Updates Pending           | False                                                                              |
| Network ID                | nng82wb                                                                            |
| Private IP Address        | 10.64.14.135                                                                       |
| Public IP Address         | None                                                                               |
| Region                    | East Coast (NY2)                                                                   |
| Script ID                 | None                                                                               |
| Last Run                  | None                                                                               |
| Dynamic Public IP         | False                                                                              |
| Last event                | name:     restart                                                                  |
|                           | state:    done                                                                     |
|                           | created:  2019-04-12T12:19:03.814Z                                                 |
+---------------------------+------------------------------------------------------------------------------------+
"""

    BASIC_COMMAND_WITH_API_KEY = [
        "machines", "details",
        "--id", "some_id",
        "--apiKey", "some_key",
    ]
    COMMAND_WITH_OPTIONS_FILE = ["machines", "details", "--optionsFile", ]  # path added in test

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Failed to fetch data: Invalid API token\n"

    RESPONSE_JSON_WHEN_MACHINE_WAS_NOT_FOUND = {
        "error": {
            "name": "Error",
            "status": 404,
            "message": "Machine not found"
        }
    }
    EXPECTED_STDOUT_WHEN_MACHINE_WAS_NOT_FOUND = "Failed to fetch data: Machine not found\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_post_request_and_print_table_when_machines_list_was_used(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON, status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        assert result.output.strip() == self.EXPECTED_STDOUT.strip(), result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=None,
                                       params=self.REQUEST_PARAMS)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_post_request_when_machines_show_was_used_with_api_key_option(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON, status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.REQUEST_PARAMS)
        assert result.output.strip() == self.EXPECTED_STDOUT.strip()
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_options_from_yaml_file(self, get_patched, machines_show_config_path):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [machines_show_config_path]

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, command)

        assert result.output.strip() == self.EXPECTED_STDOUT.strip(), result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.REQUEST_PARAMS)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_post_request_when_machines_list_was_used_with_wrong_api_key(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.REQUEST_PARAMS)
        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_error_message_when_machine_was_not_found(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WHEN_MACHINE_WAS_NOT_FOUND,
                                                status_code=404)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=None,
                                       params=self.REQUEST_PARAMS)
        assert result.output == self.EXPECTED_STDOUT_WHEN_MACHINE_WAS_NOT_FOUND
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_error_message_when_error_status_code_received_but_no_content_was_provided(self, get_patched):
        get_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=None,
                                       params=self.REQUEST_PARAMS)
        assert result.output == "Failed to fetch data\n"
        assert result.exit_code == 0


class TestStartMachine(object):
    URL = "https://api.paperspace.io/machines/some_id/start/"
    COMMAND = [
        "machines", "start",
        "--id", "some_id",
    ]
    EXPECTED_STDOUT = "Machine started\n"

    COMMAND_WITH_OPTIONS_FILE = ["machines", "start", "--optionsFile", ]  # path added in test

    COMMAND_WITH_API_KEY = [
        "machines", "start",
        "--id", "some_id",
        "--apiKey", "some_key",
    ]

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Unable to start instance: Invalid API token\n"

    RESPONSE_JSON_WITH_404_MACHINE_NOT_FOUND = {
        "error": {
            "name": "Error",
            "status": 404,
            "message": "Not found. Please contact support@paperspace.com for help."
        }
    }
    EXPECTED_STDOUT_WHEN_MACHINE_WAS_NOT_FOUND = "Unable to start instance: Not found. " \
                                                 "Please contact support@paperspace.com for help.\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_get_request_and_print_valid_message_when_start_command_was_used(self, post_patched):
        post_patched.return_value = MockResponse(status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS,
                                        json=None,
                                        params=None,
                                        files=None,
                                        data=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_changed_headers_when_api_key_option_was_used(self, post_patched):
        post_patched.return_value = MockResponse(status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY)

        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                        json=None,
                                        params=None,
                                        files=None,
                                        data=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_options_from_yaml_file(self, post_patched, machines_start_config_path):
        post_patched.return_value = MockResponse()
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [machines_start_config_path]

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                        json=None,
                                        params=None,
                                        files=None,
                                        data=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_valid_error_message_when_start_command_was_used_with_invalid_api_token(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS,
                                        json=None,
                                        params=None,
                                        files=None,
                                        data=None)
        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_valid_error_message_when_no_content_was_received_in_response(self, post_patched):
        post_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS,
                                        json=None,
                                        params=None,
                                        files=None,
                                        data=None)
        assert result.output == "Unable to start instance\n"
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_error_message_when_machine_with_given_id_was_not_found(self, post_patched):
        post_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WITH_404_MACHINE_NOT_FOUND,
                                                 status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS,
                                        json=None,
                                        params=None,
                                        files=None,
                                        data=None)
        assert result.output == self.EXPECTED_STDOUT_WHEN_MACHINE_WAS_NOT_FOUND
        assert result.exit_code == 0


class TestStopMachine(object):
    URL = "https://api.paperspace.io/machines/some_id/stop/"
    COMMAND = [
        "machines", "stop",
        "--id", "some_id",
    ]
    EXPECTED_STDOUT = "Machine stopped\n"

    COMMAND_WITH_OPTIONS_FILE = ["machines", "stop", "--optionsFile", ]  # path added in test

    COMMAND_WITH_API_KEY = [
        "machines", "stop",
        "--id", "some_id",
        "--apiKey", "some_key",
    ]

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Unable to stop instance: Invalid API token\n"

    RESPONSE_JSON_WITH_404_MACHINE_NOT_FOUND = {
        "error": {
            "name": "Error",
            "status": 404,
            "message": "Not found. Please contact support@paperspace.com for help."
        }
    }
    EXPECTED_STDOUT_WHEN_MACHINE_WAS_NOT_FOUND = "Unable to stop instance: Not found. " \
                                                 "Please contact support@paperspace.com for help.\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_get_request_and_print_valid_message_when_stop_command_was_used(self, post_patched):
        post_patched.return_value = MockResponse(status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS,
                                        json=None,
                                        params=None,
                                        files=None,
                                        data=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_changed_headers_when_api_key_option_was_used(self, post_patched):
        post_patched.return_value = MockResponse(status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY)

        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                        json=None,
                                        params=None,
                                        files=None,
                                        data=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_options_from_yaml_file(self, post_patched, machines_stop_config_path):
        post_patched.return_value = MockResponse()
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [machines_stop_config_path]

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, command)

        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                        json=None,
                                        params=None,
                                        files=None,
                                        data=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_valid_error_message_when_stop_command_was_used_with_invalid_api_token(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS,
                                        json=None,
                                        params=None,
                                        files=None,
                                        data=None)
        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_valid_error_message_when_no_content_was_received_in_response(self, post_patched):
        post_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS,
                                        json=None,
                                        params=None,
                                        files=None,
                                        data=None)
        assert result.output == "Unable to stop instance\n"
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_error_message_when_machine_with_given_id_was_not_found(self, post_patched):
        post_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WITH_404_MACHINE_NOT_FOUND,
                                                 status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=EXPECTED_HEADERS,
                                        json=None,
                                        params=None,
                                        files=None,
                                        data=None)
        assert result.output == self.EXPECTED_STDOUT_WHEN_MACHINE_WAS_NOT_FOUND
        assert result.exit_code == 0


class TestUpdateMachine(object):
    URL = "https://api.paperspace.io/machines/some_id/updateMachinePublic/"
    BASIC_COMMAND = [
        "machines", "update",
        "--id", "some_id",
        "--machineName", "some_name",
    ]
    REQUEST_JSON = {"machineName": "some_name"}

    ALL_COMMANDS = [
        "machines", "update",
        "--id", "some_id",
        "--machineName", "some_name",
        "--shutdownTimeoutInHours", "2",
        "--shutdownTimeoutForces", "true",
        "--performAutoSnapshot", "true",
        "--autoSnapshotFrequency", "hour",
        "--autoSnapshotSaveCount", "1",
        "--dynamicPublicIp", "true",
    ]
    ALL_COMMANDS_REQUEST_JSON = {
        "machineName": "some_name",
        "shutdownTimeoutInHours": 2,
        "shutdownTimeoutForces": True,
        "performAutoSnapshot": True,
        "autoSnapshotFrequency": "hour",
        "autoSnapshotSaveCount": 1,
        "dynamicPublicIp": True,
    }
    COMMAND_WITH_OPTIONS_FILE = ["machines", "update", "--optionsFile", ]  # path added in test

    BASIC_COMMAND_WITH_API_KEY = [
        "machines", "update",
        "--id", "some_id",
        "--machineName", "some_name",
        "--apiKey", "some_key",
    ]
    EXPECTED_STDOUT = "Machine updated\n"

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Failed to update resource: Invalid API token\n"

    RESPONSE_JSON_WITH_WRONG_MACHINE_ID = {"error": {"name": "Error", "status": 404, "message": "Not found"}}

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_valid_post_request_when_machine_create_was_used_with_requested_options(self, get_patched):
        get_patched.return_value = MockResponse({}, 200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=self.REQUEST_JSON,
                                       params=None,
                                       files=None,
                                       data=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_valid_post_request_when_machine_create_was_used_with_all_options(self, get_patched):
        get_patched.return_value = MockResponse({}, 200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.ALL_COMMANDS)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=self.ALL_COMMANDS_REQUEST_JSON,
                                       params=None,
                                       files=None,
                                       data=None)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_changed_headers_when_api_key_option_was_used(self, get_patched):
        get_patched.return_value = MockResponse(example_responses.CREATE_MACHINE_RESPONSE, 200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=self.REQUEST_JSON,
                                       params=None,
                                       files=None,
                                       data=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_options_from_yaml_file(self, get_patched, machines_update_config_path):
        get_patched.return_value = MockResponse(example_responses.CREATE_MACHINE_RESPONSE, 200)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [machines_update_config_path]

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, command)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=self.ALL_COMMANDS_REQUEST_JSON,
                                       params=None,
                                       files=None,
                                       data=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_error_message_when_wrong_api_key_was_used(self, get_patched):
        get_patched.return_value = MockResponse(self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, 400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=self.REQUEST_JSON,
                                       params=None,
                                       files=None,
                                       data=None)
        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_error_message_when_wrong_machine_id_was_used(self, get_patched):
        get_patched.return_value = MockResponse(self.RESPONSE_JSON_WITH_WRONG_MACHINE_ID, 400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=self.REQUEST_JSON,
                                       params=None,
                                       files=None,
                                       data=None)
        assert result.output == "Failed to update resource: Not found\n"
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_print_error_message_when_no_content_was_received_in_response(self, get_patched):
        get_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=self.REQUEST_JSON,
                                       params=None,
                                       files=None,
                                       data=None)
        assert result.output == "Failed to update resource\n"
        assert result.exit_code == 0


class TestShowMachineUtilization(object):
    URL = "https://api.paperspace.io/machines/getUtilization/"
    BASIC_COMMAND = [
        "machines", "utilization",
        "--id", "some_id",
        "--billingMonth", "2017-09",
    ]
    REQUEST_PARAMS = {"machineId": "some_id", "billingMonth": "2017-09"}
    EXPECTED_RESPONSE_JSON = example_responses.SHOW_MACHINE_UTILIZATION_RESPONSE
    EXPECTED_STDOUT = """+----------------------+---------------+
| ID                   | some_key      |
+----------------------+---------------+
| Machine Seconds used | 0             |
| Machine Hourly rate  | 0             |
| Storage Seconds Used | 256798.902394 |
| Storage Monthly Rate | 5.00          |
+----------------------+---------------+
"""

    BASIC_COMMAND_WITH_API_KEY = [
        "machines", "utilization",
        "--id", "some_id",
        "--billingMonth", "2017-09",
        "--apiKey", "some_key",
    ]

    COMMAND_WITH_OPTIONS_FILE = ["machines", "utilization", "--optionsFile", ]  # path added in test

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Failed to fetch data: Invalid API token\n"

    RESPONSE_JSON_WHEN_MACHINE_WAS_NOT_FOUND = {
        "error": {
            "name": "Error",
            "status": 404,
            "message": "Machine not found"
        }
    }
    EXPECTED_STDOUT_WHEN_MACHINE_WAS_NOT_FOUND = "Failed to fetch data: Machine not found\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_post_request_and_print_table_when_machines_utilizaation_was_used(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON, status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=None,
                                       params=self.REQUEST_PARAMS)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_post_request_when_machines_utilization_was_used_with_api_key_option(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON, status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.REQUEST_PARAMS)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_options_from_yaml_file(self, get_patched, machines_utilization_config_path):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [machines_utilization_config_path]

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, command)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.REQUEST_PARAMS)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_post_request_when_machines_utilization_was_used_with_wrong_api_key(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.REQUEST_PARAMS)
        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_error_message_when_machine_was_not_found(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WHEN_MACHINE_WAS_NOT_FOUND,
                                                status_code=404)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=None,
                                       params=self.REQUEST_PARAMS)
        assert result.output == self.EXPECTED_STDOUT_WHEN_MACHINE_WAS_NOT_FOUND
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_error_message_when_error_status_code_received_but_no_content_was_provided(self, get_patched):
        get_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=None,
                                       params=self.REQUEST_PARAMS)
        assert result.output == "Failed to fetch data\n"
        assert result.exit_code == 0


class TestWaitForMachine(object):
    URL = "https://api.paperspace.io/machines/getMachinePublic/"
    BASIC_COMMAND = [
        "machines", "waitfor",
        "--id", "some_id",
        "--state", "off",
    ]
    REQUEST_PARAMS = {"machineId": "some_id"}
    EXPECTED_RESPONSE_JSON = example_responses.SHOW_MACHINE_RESPONSE
    EXPECTED_STDOUT = "Machine state: off\n"

    BASIC_COMMAND_WITH_API_KEY = [
        "machines", "waitfor",
        "--id", "some_id",
        "--state", "off",
        "--apiKey", "some_key",
    ]

    COMMAND_WITH_OPTIONS_FILE = ["machines", "waitfor", "--optionsFile", ]  # path added in test

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Failed to fetch data: Invalid API token\n"

    RESPONSE_JSON_WHEN_MACHINE_WAS_NOT_FOUND = {
        "error": {
            "name": "Error",
            "status": 404,
            "message": "Machine not found"
        }
    }
    EXPECTED_STDOUT_WHEN_MACHINE_WAS_NOT_FOUND = "Failed to fetch data: Machine not found\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_post_request_and_print_table_when_machines_waitfor_was_used(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON, status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=None,
                                       params=self.REQUEST_PARAMS)
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_post_request_when_machines_waitfor_was_used_with_api_key_option(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON, status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.REQUEST_PARAMS)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_post_request_when_machines_waitfor_was_used_with_wrong_api_key(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.REQUEST_PARAMS)
        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_options_from_yaml_file(self, get_patched, machines_waitfor_config_path):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, status_code=400)
        command = self.COMMAND_WITH_OPTIONS_FILE[:] + [machines_waitfor_config_path]

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, command)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.REQUEST_PARAMS)
        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_error_message_when_machine_was_not_found(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WHEN_MACHINE_WAS_NOT_FOUND,
                                                status_code=404)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=None,
                                       params=self.REQUEST_PARAMS)
        assert result.output == self.EXPECTED_STDOUT_WHEN_MACHINE_WAS_NOT_FOUND
        assert result.exit_code == 0

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_print_error_message_when_error_status_code_received_but_no_content_was_provided(self, get_patched):
        get_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=EXPECTED_HEADERS,
                                       json=None,
                                       params=self.REQUEST_PARAMS)
        assert result.output == "Failed to fetch data\n"
        assert result.exit_code == 0

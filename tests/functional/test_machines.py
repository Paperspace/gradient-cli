import mock
from click.testing import CliRunner

import paperspace.client
from paperspace.cli import cli
from tests import MockResponse, example_responses


class TestMachineAvailability(object):
    URL = "https://api.paperspace.io/machines/getAvailability/"
    COMMAND = [
        "machines", "availability",
        "--region", "ny2",
        "--machineType", "P4000",
    ]
    PARAMS = {"region": "East Coast (NY2)", "machineType": "P4000"}
    RESPONSE_JSON = {"available": True}
    EXPECTED_HEADERS = paperspace.client.default_headers.copy()

    COMMAND_WITH_API_KEY = [
        "machines", "availability",
        "--region", "ny2",
        "--machineType", "P4000",
        "--apiKey", "some_key",
    ]
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = paperspace.client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"
    EXPECTED_STDOUT = "Machine available: True\n"

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Invalid API token\n"

    @mock.patch("paperspace.client.requests.get")
    def test_should_send_get_request_and_print_valid_message_when_availability_command_was_used(self, get_patched):
        get_patched.return_value = MockResponse(self.RESPONSE_JSON, 200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=None,
                                       params=self.PARAMS)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.get")
    def test_should_send_changed_headers_when_api_key_option_was_used(self, get_patched):
        get_patched.return_value = MockResponse(self.RESPONSE_JSON, 200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.PARAMS)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.get")
    def test_should_print_valid_error_message_when_availability_command_was_used_with_invalid_api_token(self,
                                                                                                        get_patched):
        get_patched.return_value = MockResponse(self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, 400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=None,
                                       params=self.PARAMS)
        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.get")
    def test_should_print_valid_error_message_when_no_content_was_received_in_response(self, get_patched):
        get_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=None,
                                       params=self.PARAMS)
        assert result.output == "Unknown error while checking machine availability\n"
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.get")
    def test_should_print_valid_error_message_when_no_content_was_received_in_response(self, get_patched):
        get_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=None,
                                       params=self.PARAMS)
        assert result.output == "Unknown error while checking machine availability\n"
        assert result.exit_code == 0


class TestCreateMachine(object):
    URL = "https://api.paperspace.io/machines/createSingleMachinePublic/"
    BASIC_COMMAND = [
        "machines", "create",
        "--region", "CA1",
        "--machineType", "P5000",
        "--size", 2,
        "--billingType", "hourly",
        "--machineName", "some_name",
        "--templateId", "some_template",
    ]
    REQUEST_JSON = {
        "billingType": "hourly",
        "machineType": "P5000",
        "machineName": "some_name",
        "region": "West Coast (CA1)",
        "templateId": "some_template",
        "size": 2,
    }
    EXPECTED_HEADERS = paperspace.client.default_headers.copy()

    ALL_COMMANDS = [
        "machines", "create",
        "--region", "CA1",
        "--machineType", "P5000",
        "--size", 2,
        "--billingType", "hourly",
        "--machineName", "some_name",
        "--templateId", "some_template_ip",
        "--dynamicPublicIp",
        "--email", "some@email.com",
        "--password", "some_password",
        "--firstName", "first_name",
        "--lastName", "last_name",
        "--notificationEmail", "other@email.com",
        "--scriptId", "some_script_id"
    ]
    ALL_COMMANDS_REQUEST_JSON = {
        "region": "West Coast (CA1)",
        "machineType": "P5000",
        "size": 2,
        "billingType": "hourly",
        "machineName": "some_name",
        "templateId": "some_template_ip",
        "dynamicPublicIp": True,
        "email": "some@email.com",
        "password": "some_password",
        "firstName": "first_name",
        "lastName": "last_name",
        "notificationEmail": "other@email.com",
        "scriptId": "some_script_id",
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
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = paperspace.client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"
    EXPECTED_STDOUT = "New machine created with id: psclbvqpc\n"

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Invalid API token\n"

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
        "--teamId", "some_user_id",
        "--email", "some@email.com",
    ]

    @mock.patch("paperspace.client.requests.post")
    def test_should_send_valid_post_request_when_machine_create_was_used_with_requested_options(self, get_patched):
        get_patched.return_value = MockResponse(example_responses.CREATE_MACHINE_RESPONSE, 200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=self.REQUEST_JSON,
                                       params=None,
                                       files=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.post")
    def test_should_send_valid_post_request_when_machine_create_was_used_with_all_options(self, get_patched):
        get_patched.return_value = MockResponse(example_responses.CREATE_MACHINE_RESPONSE, 200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.ALL_COMMANDS)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=self.ALL_COMMANDS_REQUEST_JSON,
                                       params=None,
                                       files=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.post")
    def test_should_send_changed_headers_when_api_key_option_was_used(self, get_patched):
        get_patched.return_value = MockResponse(example_responses.CREATE_MACHINE_RESPONSE, 200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=self.REQUEST_JSON,
                                       params=None,
                                       files=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.post")
    def test_should_print_error_message_when_wrong_api_key_was_used(self, get_patched):
        get_patched.return_value = MockResponse(self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, 400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=self.REQUEST_JSON,
                                       params=None,
                                       files=None)
        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.post")
    def test_should_print_error_message_when_wrong_template_id_was_used(self, get_patched):
        get_patched.return_value = MockResponse(self.RESPONSE_JSON_WITH_WRONG_TEMPLATE_ID, 400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=self.REQUEST_JSON,
                                       params=None,
                                       files=None)
        assert result.output == "templateId not found\n"
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.post")
    def test_should_print_error_message_when_no_content_was_received_in_response(self, get_patched):
        get_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=self.REQUEST_JSON,
                                       params=None,
                                       files=None)
        assert result.output == "Unknown error while creating machine\n"
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.post")
    def test_should_print_error_message_when_mutually_exclusive_options_were_used(self, get_patched):
        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_MUTUALLY_EXCLUSIVE_OPTIONS_USED)

        get_patched.assert_not_called()
        assert "Error: --userId is mutually exclusive with --email, --password, --firstName and --lastName\n" \
               in result.output
        assert result.exit_code == 2


class TestDestroyMachine(object):
    URL = "https://api.paperspace.io/machines/some_machine_id/destroyMachine/"
    BASIC_COMMAND = [
        "machines", "destroy",
        "--machineId", "some_machine_id",
    ]
    EXPECTED_HEADERS = paperspace.client.default_headers.copy()

    ALL_COMMANDS = [
        "machines", "destroy",
        "--machineId", "some_machine_id",
        "--releasePublicIp",
    ]
    ALL_COMMANDS_REQUEST_JSON = {"releasePublicIp": True}

    BASIC_COMMAND_WITH_API_KEY = [
        "machines", "destroy",
        "--machineId", "some_machine_id",
        "--apiKey", "some_key",
    ]
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = paperspace.client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"
    EXPECTED_STDOUT = "Machine successfully destroyed\n"

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Invalid API token\n"

    RESPONSE_JSON_WITH_404_MACHINE_NOT_FOUND = {
        "error": {
            "name": "Error",
            "status": 404,
            "message": "Not found. Please contact support@paperspace.com for help."
        }
    }
    EXPECTED_STDOUT_WHEN_MACHINE_WAS_NOT_FOUND = "Not found. Please contact support@paperspace.com for help.\n"

    @mock.patch("paperspace.client.requests.post")
    def test_should_send_valid_post_request_when_machines_destroy_was_used(self, post_patched):
        post_patched.return_value = MockResponse(status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=self.EXPECTED_HEADERS,
                                        json=None,
                                        params=None,
                                        files=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.post")
    def test_should_send_valid_post_request_when_machines_destroy_was_used_with_all_options(self, post_patched):
        post_patched.return_value = MockResponse(status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.ALL_COMMANDS)

        post_patched.assert_called_with(self.URL,
                                        headers=self.EXPECTED_HEADERS,
                                        json=self.ALL_COMMANDS_REQUEST_JSON,
                                        params=None,
                                        files=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.post")
    def test_should_send_valid_post_request_when_machines_destroy_was_used_with_api_key_option(self, post_patched):
        post_patched.return_value = MockResponse(status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        post_patched.assert_called_with(self.URL,
                                        headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                        json=None,
                                        params=None,
                                        files=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.post")
    def test_should_send_valid_post_request_when_machines_destroy_was_used_with_wrong_api_key(self, post_patched):
        post_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=self.EXPECTED_HEADERS,
                                        json=None,
                                        params=None,
                                        files=None)
        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.post")
    def test_should_print_error_message_when_machine_with_given_id_was_not_found(self, post_patched):
        post_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WITH_404_MACHINE_NOT_FOUND,
                                                 status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=self.EXPECTED_HEADERS,
                                        json=None,
                                        params=None,
                                        files=None)
        assert result.output == self.EXPECTED_STDOUT_WHEN_MACHINE_WAS_NOT_FOUND
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.post")
    def test_should_print_error_message_when_error_status_code_received_but_no_content_was_provided(self, post_patched):
        post_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=self.EXPECTED_HEADERS,
                                        json=None,
                                        params=None,
                                        files=None)
        assert result.output == "Unknown error while destroying the machine\n"
        assert result.exit_code == 0


class TestListMachines(object):
    URL = "https://api.paperspace.io/machines/getMachines/"
    EXPECTED_HEADERS = paperspace.client.default_headers.copy()
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

    ALL_COMMANDS = [
        "machines", "list",
        "--machineId", "some_machine_id",
        "--name", "some_name",
        "--os", "some_os",
        "--ram", 123456789,
        "--cpus", 2,
        "--gpu", "GeForce2MX",
        "--storageTotal", "321432543",
        "--storageUsed", "234345456",
        "--usageRate", "C1 Hourly",
        "--shutdownTimeoutInHours", 2,
        "--performAutoSnapshot", "true",
        "--autoSnapshotFrequency", "hour",
        "--autoSnapshotSaveCount", 5,
        "--agentType", "LinuxHeadless",
        "--dtCreated", "2017-09-17T05:55:29.665Z",
        "--state", "ready",
        "--updatesPending", "False",
        "--networkId", "asdf",
        "--privateIpAddress", "192.168.0.1",
        "--publicIpAddress", "104.25.94.37",
        "--region", "CA1",
        "--userId", "alskdjf",
        "--teamId", "qpwoeirut",
        "--dtLastRun", "2019-04-11T18:10:29.665Z"
    ]
    ALL_COMMANDS_REQUEST_JSON = {
        "params": {
            "ram": 123456789,
            "userId": "alskdjf",
            "cpus": 2,
            "teamId": "qpwoeirut",
            "updatesPending": "False",
            "networkId": "asdf",
            "storageTotal": "321432543",
            "shutdownTimeoutInHours": 2,
            "state": "ready",
            "usageRate": "C1 Hourly",
            "publicIpAddress": "104.25.94.37",
            "gpu": "GeForce2MX",
            "privateIpAddress": "192.168.0.1",
            "dtCreated": "2017-09-17T05:55:29.665Z",
            "dtLastRun": "2019-04-11T18:10:29.665Z",
            "storageUsed": "234345456",
            "autoSnapshotSaveCount": 5,
            "name": "some_name",
            "machineId": "some_machine_id",
            "region": "West Coast (CA1)",
            "performAutoSnapshot": True,
            "autoSnapshotFrequency": "hour",
            "os": "some_os",
            "agentType": "LinuxHeadless"
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

    BASIC_COMMAND_WITH_API_KEY = ["machines", "list", "--apiKey", "some_key"]
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = paperspace.client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Invalid API token\n"

    EXPECTED_STDOUT_WHEN_NO_MACHINES_WERE_FOUND = "No data found\n"

    COMMAND_WITH_MUTUALLY_EXCLUSIVE_OPTIONS = [
        "machines", "list",
        "--params", '{"cpus":2,"gpu":"ATIRage128"}',
        "--name", "some_name",
    ]

    @mock.patch("paperspace.client.requests.get")
    def test_should_send_valid_post_request_and_print_table_when_machines_list_was_used(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON, status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=None,
                                       params=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.get")
    def test_should_send_valid_post_request_when_all_options_were_used(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON, status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.ALL_COMMANDS)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=self.ALL_COMMANDS_REQUEST_JSON,
                                       params=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.get")
    def test_should_send_valid_post_request_when_params_option_was_used(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON, status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND_WITH_PARAMS_OPTION)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=self.REQUEST_JSON_WITH_PARAMS_OPTION,
                                       params=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.get")
    def test_should_send_valid_post_request_when_machines_list_was_used_with_api_key_option(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON, status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.get")
    def test_should_send_valid_post_request_when_machines_list_was_used_with_wrong_api_key(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=None)
        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.get")
    def test_should_print_error_message_when_no_machine_was_not_found(self, get_patched):
        get_patched.return_value = MockResponse(json_data=[], status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=None,
                                       params=None)
        assert result.output == self.EXPECTED_STDOUT_WHEN_NO_MACHINES_WERE_FOUND
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.get")
    def test_should_print_error_message_when_error_status_code_received_but_no_content_was_provided(self, get_patched):
        get_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=None,
                                       params=None)
        assert result.output == "Error while parsing response data: No JSON\n"
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.get")
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
        "--machineId", "some_id",
    ]
    EXPECTED_HEADERS = paperspace.client.default_headers.copy()
    EXPECTED_STDOUT = "Machine restarted\n"

    COMMAND_WITH_API_KEY = [
        "machines", "restart",
        "--machineId", "some_id",
        "--apiKey", "some_key",
    ]
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = paperspace.client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Invalid API token\n"

    RESPONSE_JSON_WITH_404_MACHINE_NOT_FOUND = {
        "error": {
            "name": "Error",
            "status": 404,
            "message": "Not found. Please contact support@paperspace.com for help."
        }
    }
    EXPECTED_STDOUT_WHEN_MACHINE_WAS_NOT_FOUND = "Not found. Please contact support@paperspace.com for help.\n"

    @mock.patch("paperspace.client.requests.post")
    def test_should_send_get_request_and_print_valid_message_when_restart_command_was_used(self, post_patched):
        post_patched.return_value = MockResponse(status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=self.EXPECTED_HEADERS,
                                        json=None,
                                        params=None,
                                        files=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.post")
    def test_should_send_changed_headers_when_api_key_option_was_used(self, post_patched):
        post_patched.return_value = MockResponse(status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY)

        post_patched.assert_called_with(self.URL,
                                        headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                        json=None,
                                        params=None,
                                        files=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.post")
    def test_should_print_valid_error_message_when_start_command_was_used_with_invalid_api_token(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=self.EXPECTED_HEADERS,
                                        json=None,
                                        params=None,
                                        files=None)
        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.post")
    def test_should_print_valid_error_message_when_no_content_was_received_in_response(self, post_patched):
        post_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=self.EXPECTED_HEADERS,
                                        json=None,
                                        params=None,
                                        files=None)
        assert result.output == "Unknown error while restarting the machine\n"
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.post")
    def test_should_print_error_message_when_machine_with_given_id_was_not_found(self, post_patched):
        post_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WITH_404_MACHINE_NOT_FOUND,
                                                 status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=self.EXPECTED_HEADERS,
                                        json=None,
                                        params=None,
                                        files=None)
        assert result.output == self.EXPECTED_STDOUT_WHEN_MACHINE_WAS_NOT_FOUND
        assert result.exit_code == 0


class TestShowMachine(object):
    URL = "https://api.paperspace.io/machines/getMachinePublic/"
    EXPECTED_HEADERS = paperspace.client.default_headers.copy()
    BASIC_COMMAND = ["machines", "show", "--machineId", "psbtuwfvt"]
    REQUEST_PARAMS = {"machineId": "psbtuwfvt"}
    EXPECTED_RESPONSE_JSON = example_responses.SHOW_MACHINE_RESPONSE
    EXPECTED_STDOUT = """+---------------------------+------------------------------------------------------------------------------------+
| ID                        | psbtuwfvt                                                                          |
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
| Last event                | name:     create                                                                   |
|                           | state:    done                                                                     |
|                           | created:  None                                                                     |
+---------------------------+------------------------------------------------------------------------------------+
"""

    BASIC_COMMAND_WITH_API_KEY = [
        "machines", "show",
        "--machineId", "psbtuwfvt",
        "--apiKey", "some_key",
    ]
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = paperspace.client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Invalid API token\n"

    RESPONSE_JSON_WHEN_MACHINE_WAS_NOT_FOUND = {
        "error": {
            "name": "Error",
            "status": 404,
            "message": "Machine not found"
        }
    }
    EXPECTED_STDOUT_WHEN_MACHINE_WAS_NOT_FOUND = "Machine not found\n"

    @mock.patch("paperspace.client.requests.get")
    def test_should_send_valid_post_request_and_print_table_when_machines_list_was_used(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON, status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=None,
                                       params=self.REQUEST_PARAMS)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.get")
    def test_should_send_valid_post_request_when_machines_list_was_used_with_api_key_option(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON, status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.REQUEST_PARAMS)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.get")
    def test_should_send_valid_post_request_when_machines_list_was_used_with_wrong_api_key(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.REQUEST_PARAMS)
        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.get")
    def test_should_print_error_message_when_machine_was_not_found(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WHEN_MACHINE_WAS_NOT_FOUND,
                                                status_code=404)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=None,
                                       params=self.REQUEST_PARAMS)
        assert result.output == self.EXPECTED_STDOUT_WHEN_MACHINE_WAS_NOT_FOUND
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.get")
    def test_should_print_error_message_when_error_status_code_received_but_no_content_was_provided(self, get_patched):
        get_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=None,
                                       params=self.REQUEST_PARAMS)
        assert result.output == "Error while parsing response data: No JSON\n"
        assert result.exit_code == 0


class TestStartMachine(object):
    URL = "https://api.paperspace.io/machines/some_id/start/"
    COMMAND = [
        "machines", "start",
        "--machineId", "some_id",
    ]
    EXPECTED_HEADERS = paperspace.client.default_headers.copy()
    EXPECTED_STDOUT = "Machine started\n"

    COMMAND_WITH_API_KEY = [
        "machines", "start",
        "--machineId", "some_id",
        "--apiKey", "some_key",
    ]
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = paperspace.client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Invalid API token\n"

    RESPONSE_JSON_WITH_404_MACHINE_NOT_FOUND = {
        "error": {
            "name": "Error",
            "status": 404,
            "message": "Not found. Please contact support@paperspace.com for help."
        }
    }
    EXPECTED_STDOUT_WHEN_MACHINE_WAS_NOT_FOUND = "Not found. Please contact support@paperspace.com for help.\n"

    @mock.patch("paperspace.client.requests.post")
    def test_should_send_get_request_and_print_valid_message_when_start_command_was_used(self, post_patched):
        post_patched.return_value = MockResponse(status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=self.EXPECTED_HEADERS,
                                        json=None,
                                        params=None,
                                        files=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.post")
    def test_should_send_changed_headers_when_api_key_option_was_used(self, post_patched):
        post_patched.return_value = MockResponse(status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY)

        post_patched.assert_called_with(self.URL,
                                        headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                        json=None,
                                        params=None,
                                        files=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.post")
    def test_should_print_valid_error_message_when_start_command_was_used_with_invalid_api_token(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=self.EXPECTED_HEADERS,
                                        json=None,
                                        params=None,
                                        files=None)
        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.post")
    def test_should_print_valid_error_message_when_no_content_was_received_in_response(self, post_patched):
        post_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=self.EXPECTED_HEADERS,
                                        json=None,
                                        params=None,
                                        files=None)
        assert result.output == "Unknown error while starting the machine\n"
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.post")
    def test_should_print_error_message_when_machine_with_given_id_was_not_found(self, post_patched):
        post_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WITH_404_MACHINE_NOT_FOUND,
                                                 status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=self.EXPECTED_HEADERS,
                                        json=None,
                                        params=None,
                                        files=None)
        assert result.output == self.EXPECTED_STDOUT_WHEN_MACHINE_WAS_NOT_FOUND
        assert result.exit_code == 0


class TestStopMachine(object):
    URL = "https://api.paperspace.io/machines/some_id/stop/"
    COMMAND = [
        "machines", "stop",
        "--machineId", "some_id",
    ]
    EXPECTED_HEADERS = paperspace.client.default_headers.copy()
    EXPECTED_STDOUT = "Machine stopped\n"

    COMMAND_WITH_API_KEY = [
        "machines", "stop",
        "--machineId", "some_id",
        "--apiKey", "some_key",
    ]
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = paperspace.client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Invalid API token\n"

    RESPONSE_JSON_WITH_404_MACHINE_NOT_FOUND = {
        "error": {
            "name": "Error",
            "status": 404,
            "message": "Not found. Please contact support@paperspace.com for help."
        }
    }
    EXPECTED_STDOUT_WHEN_MACHINE_WAS_NOT_FOUND = "Not found. Please contact support@paperspace.com for help.\n"

    @mock.patch("paperspace.client.requests.post")
    def test_should_send_get_request_and_print_valid_message_when_stop_command_was_used(self, post_patched):
        post_patched.return_value = MockResponse(status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=self.EXPECTED_HEADERS,
                                        json=None,
                                        params=None,
                                        files=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.post")
    def test_should_send_changed_headers_when_api_key_option_was_used(self, post_patched):
        post_patched.return_value = MockResponse(status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY)

        post_patched.assert_called_with(self.URL,
                                        headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                        json=None,
                                        params=None,
                                        files=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.post")
    def test_should_print_valid_error_message_when_stop_command_was_used_with_invalid_api_token(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=self.EXPECTED_HEADERS,
                                        json=None,
                                        params=None,
                                        files=None)
        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.post")
    def test_should_print_valid_error_message_when_no_content_was_received_in_response(self, post_patched):
        post_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=self.EXPECTED_HEADERS,
                                        json=None,
                                        params=None,
                                        files=None)
        assert result.output == "Unknown error while stopping the machine\n"
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.post")
    def test_should_print_error_message_when_machine_with_given_id_was_not_found(self, post_patched):
        post_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WITH_404_MACHINE_NOT_FOUND,
                                                 status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.COMMAND)

        post_patched.assert_called_with(self.URL,
                                        headers=self.EXPECTED_HEADERS,
                                        json=None,
                                        params=None,
                                        files=None)
        assert result.output == self.EXPECTED_STDOUT_WHEN_MACHINE_WAS_NOT_FOUND
        assert result.exit_code == 0


class TestUpdateMachine(object):
    URL = "https://api.paperspace.io/machines/some_id/updateMachinePublic/"
    BASIC_COMMAND = [
        "machines", "update",
        "--machineId", "some_id",
        "--machineName", "some_name",
    ]
    REQUEST_JSON = {"machineName": "some_name"}
    EXPECTED_HEADERS = paperspace.client.default_headers.copy()

    ALL_COMMANDS = [
        "machines", "update",
        "--machineId", "some_id",
        "--machineName", "some_name",
        "--shutdownTimeoutInHours", 2,
        "--shutdownTimeoutForces", "true",
        "--performAutoSnapshot", "0",
        "--autoSnapshotFrequency", "hour",
        "--autoSnapshotSaveCount", 1,
        "--dynamicPublicIp", "f"
    ]
    ALL_COMMANDS_REQUEST_JSON = {
        "machineName": "some_name",
        "shutdownTimeoutInHours": 2,
        "shutdownTimeoutForces": True,
        "performAutoSnapshot": False,
        "autoSnapshotFrequency": "hour",
        "autoSnapshotSaveCount": 1,
        "dynamicPublicIp": False,
    }

    BASIC_COMMAND_WITH_API_KEY = [
        "machines", "update",
        "--machineId", "some_id",
        "--machineName", "some_name",
        "--apiKey", "some_key",
    ]
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = paperspace.client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"
    EXPECTED_STDOUT = "Machine updated\n"

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Invalid API token\n"

    RESPONSE_JSON_WITH_WRONG_MACHINE_ID = {"error": {"name": "Error", "status": 404, "message": "Not found"}}

    @mock.patch("paperspace.client.requests.post")
    def test_should_send_valid_post_request_when_machine_create_was_used_with_requested_options(self, get_patched):
        get_patched.return_value = MockResponse({}, 200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=self.REQUEST_JSON,
                                       params=None,
                                        files=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.post")
    def test_should_send_valid_post_request_when_machine_create_was_used_with_all_options(self, get_patched):
        get_patched.return_value = MockResponse({}, 200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.ALL_COMMANDS)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=self.ALL_COMMANDS_REQUEST_JSON,
                                       params=None,
                                        files=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.post")
    def test_should_send_changed_headers_when_api_key_option_was_used(self, get_patched):
        get_patched.return_value = MockResponse(example_responses.CREATE_MACHINE_RESPONSE, 200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=self.REQUEST_JSON,
                                       params=None,
                                        files=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.post")
    def test_should_print_error_message_when_wrong_api_key_was_used(self, get_patched):
        get_patched.return_value = MockResponse(self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, 400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=self.REQUEST_JSON,
                                       params=None,
                                       files=None)
        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.post")
    def test_should_print_error_message_when_wrong_machine_id_was_used(self, get_patched):
        get_patched.return_value = MockResponse(self.RESPONSE_JSON_WITH_WRONG_MACHINE_ID, 400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=self.REQUEST_JSON,
                                       params=None,
                                        files=None)
        assert result.output == "Not found\n"
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.post")
    def test_should_print_error_message_when_no_content_was_received_in_response(self, get_patched):
        get_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=self.REQUEST_JSON,
                                       params=None,
                                       files=None)
        assert result.output == "Unknown error while updating machine\n"
        assert result.exit_code == 0


class TestShowMachineUtilization(object):
    URL = "https://api.paperspace.io/machines/getUtilization/"
    EXPECTED_HEADERS = paperspace.client.default_headers.copy()
    BASIC_COMMAND = [
        "machines", "utilization",
        "--machineId", "psbtuwfvt",
        "--billingMonth", "2019-04",
    ]
    REQUEST_PARAMS = {"machineId": "psbtuwfvt", "billingMonth": "2019-04"}
    EXPECTED_RESPONSE_JSON = example_responses.SHOW_MACHINE_UTILIZATION_RESPONSE
    EXPECTED_STDOUT = """+----------------------+---------------+
| ID                   | psbtuwfvt     |
+----------------------+---------------+
| Machine Seconds used | 0             |
| Machine Hourly rate  | 0             |
| Storage Seconds Used | 256798.902394 |
| Storage Monthly Rate | 5.00          |
+----------------------+---------------+
"""

    BASIC_COMMAND_WITH_API_KEY = [
        "machines", "utilization",
        "--machineId", "psbtuwfvt",
        "--billingMonth", "2019-04",
        "--apiKey", "some_key",
    ]
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = paperspace.client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Invalid API token\n"

    RESPONSE_JSON_WHEN_MACHINE_WAS_NOT_FOUND = {
        "error": {
            "name": "Error",
            "status": 404,
            "message": "Machine not found"
        }
    }
    EXPECTED_STDOUT_WHEN_MACHINE_WAS_NOT_FOUND = "Machine not found\n"

    @mock.patch("paperspace.client.requests.get")
    def test_should_send_valid_post_request_and_print_table_when_machines_utilizaation_was_used(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON, status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=None,
                                       params=self.REQUEST_PARAMS)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.get")
    def test_should_send_valid_post_request_when_machines_utilization_was_used_with_api_key_option(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON, status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.REQUEST_PARAMS)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.get")
    def test_should_send_valid_post_request_when_machines_utilization_was_used_with_wrong_api_key(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.REQUEST_PARAMS)
        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.get")
    def test_should_print_error_message_when_machine_was_not_found(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WHEN_MACHINE_WAS_NOT_FOUND,
                                                status_code=404)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=None,
                                       params=self.REQUEST_PARAMS)
        assert result.output == self.EXPECTED_STDOUT_WHEN_MACHINE_WAS_NOT_FOUND
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.get")
    def test_should_print_error_message_when_error_status_code_received_but_no_content_was_provided(self, get_patched):
        get_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=None,
                                       params=self.REQUEST_PARAMS)
        assert result.output == "Error while parsing response data: No JSON\n"
        assert result.exit_code == 0


class TestWaitForMachine(object):
    URL = "https://api.paperspace.io/machines/getMachinePublic/"
    EXPECTED_HEADERS = paperspace.client.default_headers.copy()
    BASIC_COMMAND = [
        "machines", "waitfor",
        "--machineId", "psbtuwfvt",
        "--state", "off",
    ]
    REQUEST_PARAMS = {"machineId": "psbtuwfvt"}
    EXPECTED_RESPONSE_JSON = example_responses.SHOW_MACHINE_RESPONSE
    EXPECTED_STDOUT = "Machine state: off\n"

    BASIC_COMMAND_WITH_API_KEY = [
        "machines", "waitfor",
        "--machineId", "psbtuwfvt",
        "--state", "off",
        "--apiKey", "some_key",
    ]
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = paperspace.client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"status": 400, "message": "Invalid API token"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Invalid API token\nError while reading machine state\n"

    RESPONSE_JSON_WHEN_MACHINE_WAS_NOT_FOUND = {
        "error": {
            "name": "Error",
            "status": 404,
            "message": "Machine not found"
        }
    }
    EXPECTED_STDOUT_WHEN_MACHINE_WAS_NOT_FOUND = "Machine not found\nError while reading machine state\n"

    @mock.patch("paperspace.client.requests.get")
    def test_should_send_valid_post_request_and_print_table_when_machines_waitfor_was_used(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON, status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=None,
                                       params=self.REQUEST_PARAMS)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.get")
    def test_should_send_valid_post_request_when_machines_waitfor_was_used_with_api_key_option(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.EXPECTED_RESPONSE_JSON, status_code=200)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.REQUEST_PARAMS)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.get")
    def test_should_send_valid_post_request_when_machines_waitfor_was_used_with_wrong_api_key(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WITH_WRONG_API_TOKEN, status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND_WITH_API_KEY)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                       json=None,
                                       params=self.REQUEST_PARAMS)
        assert result.output == self.EXPECTED_STDOUT_WITH_WRONG_API_TOKEN
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.get")
    def test_should_print_error_message_when_machine_was_not_found(self, get_patched):
        get_patched.return_value = MockResponse(json_data=self.RESPONSE_JSON_WHEN_MACHINE_WAS_NOT_FOUND,
                                                status_code=404)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=None,
                                       params=self.REQUEST_PARAMS)
        assert result.output == self.EXPECTED_STDOUT_WHEN_MACHINE_WAS_NOT_FOUND
        assert result.exit_code == 0

    @mock.patch("paperspace.client.requests.get")
    def test_should_print_error_message_when_error_status_code_received_but_no_content_was_provided(self, get_patched):
        get_patched.return_value = MockResponse(status_code=400)

        cli_runner = CliRunner()
        result = cli_runner.invoke(cli.cli, self.BASIC_COMMAND)

        get_patched.assert_called_with(self.URL,
                                       headers=self.EXPECTED_HEADERS,
                                       json=None,
                                       params=self.REQUEST_PARAMS)
        assert result.output == "Unknown error while reading machine state\n"
        assert result.exit_code == 0

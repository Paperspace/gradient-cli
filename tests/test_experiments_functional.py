import mock
from click.testing import CliRunner

from paperspace import cli, constants, commands


class MockResponse:
    def __init__(self, json_data, status_code, content):
        self.json_data = json_data
        self.status_code = status_code
        self.content = content

    @property
    def ok(self):
        return 200 <= self.status_code <= 299

    def json(self):
        return self.json_data


class TestExperimentsCreateSingleNode(object):
    URL = "https://services.paperspace.io/experiments/v1/experiments/"
    EXPECTED_HEADERS = commands.default_headers
    BASIC_OPTIONS_COMMAND = [
        "experiments", "create", "singlenode",
        "--name", "exp1",
        "--projectHandle", "testHandle",
        "--container", "testContainer",
        "--machineType", "testType",
        "--command", "testCommand",
        "--workspaceUrl", "some-workspace",
    ]
    FULL_OPTIONS_COMMAND = [
        "experiments", "create", "singlenode",
        "--name", "exp1",
        "--ports", 4567,
        "--workspaceUrl", "wsp.url",
        "--workingDirectory", "/work/dir/",
        "--artifactDirectory", "/artifact/dir/",
        "--clusterId", 42,
        "--experimentEnv", '{"key":"val"}',
        "--triggerEventId", 45678,
        "--projectId", 987654,
        "--projectHandle", "testHandle",
        "--container", "testContainer",
        "--machineType", "testType",
        "--command", "testCommand",
        "--count", 2,
        "--containerUser", "conUser",
        "--registryUsername", "userName",
        "--registryPassword", "passwd",
    ]
    BASIC_OPTIONS_REQUEST = {
        "name": u"exp1",
        "projectHandle": u"testHandle",
        "container": u"testContainer",
        "machineType": u"testType",
        "command": u"testCommand",
        "experimentTypeId": constants.ExperimentType.SINGLE_NODE,
        "workspaceUrl": u"some-workspace",
    }
    FULL_OPTIONS_REQUEST = {
        "name": u"exp1",
        "ports": 4567,
        "workspaceUrl": u"wsp.url",
        "workingDirectory": u"/work/dir/",
        "artifactDirectory": u"/artifact/dir/",
        "clusterId": 42,
        "experimentEnv": {u"key": u"val"},
        "triggerEventId": 45678,
        "projectId": 987654,
        "projectHandle": u"testHandle",
        "container": u"testContainer",
        "machineType": u"testType",
        "command": u"testCommand",
        "count": 2,
        "containerUser": u"conUser",
        "registryUsername": u"userName",
        "registryPassword": u"passwd",
        "experimentTypeId": constants.ExperimentType.SINGLE_NODE,
    }
    RESPONSE_JSON_200 = {"handle": "sadkfhlskdjh", "message": "success"}
    RESPONSE_CONTENT_200 = b'{"handle":"sadkfhlskdjh","message":"success"}\n'
    EXPECTED_STDOUT = "New experiment created with handle: sadkfhlskdjh\n"

    RESPONSE_JSON_404_PROJECT_NOT_FOUND = {"details": {"handle": "wrong_handle"}, "error": "Project not found"}
    RESPONSE_CONTENT_404_PROJECT_NOT_FOUND = b'{"details":{"handle":"wrong_handle"},"error":"Project not found"}\n'
    EXPECTED_STDOUT_PROJECT_NOT_FOUND = "Project not found\nhandle: wrong_handle\n"

    @mock.patch("paperspace.cli.commands.client.requests.post")
    def test_should_send_proper_data_and_print_message_when_create_experiment_was_run_with_basic_options(self,
                                                                                                         post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200, 200, self.RESPONSE_CONTENT_200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND)

        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS,
                                             json=self.BASIC_OPTIONS_REQUEST,
                                             params=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.cli.commands.client.requests.post")
    def test_should_send_proper_data_and_print_message_when_create_experiment_was_run_with_full_options(self,
                                                                                                        post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200, 200, self.RESPONSE_CONTENT_200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.FULL_OPTIONS_COMMAND)

        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS,
                                             json=self.FULL_OPTIONS_REQUEST,
                                             params=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.cli.commands.client.requests.post")
    def test_should_send_proper_data_and_print_message_when_create_wrong_project_handle_was_given(self, post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_404_PROJECT_NOT_FOUND, 404,
                                                 self.RESPONSE_CONTENT_404_PROJECT_NOT_FOUND)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND)

        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS,
                                             json=self.BASIC_OPTIONS_REQUEST,
                                             params=None)
        assert result.output == self.EXPECTED_STDOUT_PROJECT_NOT_FOUND
        assert result.exit_code == 0


class TestExperimentsCreateMultiNode(object):
    URL = "https://services.paperspace.io/experiments/v1/experiments/"
    EXPECTED_HEADERS = commands.default_headers
    BASIC_OPTIONS_COMMAND = [
        "experiments", "create", "multinode",
        "--name", "multinode_mpi",
        "--projectHandle", "prq70zy79",
        "--experimentTypeId", "GRPC",
        "--workerContainer", "wcon",
        "--workerMachineType", "mty",
        "--workerCommand", "wcom",
        "--workerCount", 2,
        "--parameterServerContainer", "pscon",
        "--parameterServerMachineType", "psmtype",
        "--parameterServerCommand", "ls",
        "--parameterServerCount", 2,
        "--workerContainerUser", "usr",
        "--workspaceUrl", "some-workspace",
    ]
    FULL_OPTIONS_COMMAND = [
        "experiments", "create", "multinode",
        "--name", "multinode_mpi",
        "--ports", 3456,
        "--workspaceUrl", "wurl",
        "--workingDirectory", "/dir",
        "--artifactDirectory", "/artdir",
        "--clusterId", 2,
        "--experimentEnv", '{"key":"val"}',
        "--triggerEventId", 12,
        "--projectId", 34,
        "--projectHandle", "prq70zy79",
        "--experimentTypeId", "MPI",
        "--workerContainer", "wcon",
        "--workerMachineType", "mty",
        "--workerCommand", "wcom",
        "--workerCount", 2,
        "--parameterServerContainer", "pscon",
        "--parameterServerMachineType", "psmtype",
        "--parameterServerCommand", "ls",
        "--parameterServerCount", 2,
        "--workerContainerUser", "usr",
        "--workerRegistryUsername", "rusr",
        "--workerRegistryPassword", "rpass",
        "--parameterServerContainerUser", "pscuser",
        "--parameterServerRegistryContainerUser", "psrcus",
        "--parameterServerRegistryPassword", "psrpass",
    ]
    BASIC_OPTIONS_REQUEST = {
        "name": u"multinode_mpi",
        "projectHandle": u"prq70zy79",
        "experimentTypeId": 2,
        "workerContainer": u"wcon",
        "workerMachineType": u"mty",
        "workerCommand": u"wcom",
        "workerCount": 2,
        "parameterServerContainer": u"pscon",
        "parameterServerMachineType": u"psmtype",
        "parameterServerCommand": u"ls",
        "parameterServerCount": 2,
        "workerContainerUser": u"usr",
        "workspaceUrl": "some-workspace",
    }
    FULL_OPTIONS_REQUEST = {
        "name": u"multinode_mpi",
        "ports": 3456,
        "workspaceUrl": u"wurl",
        "workingDirectory": u"/dir",
        "artifactDirectory": u"/artdir",
        "clusterId": 2,
        "experimentEnv": {"key": "val"},
        "triggerEventId": 12,
        "projectId": 34,
        "projectHandle": u"prq70zy79",
        "experimentTypeId": 3,
        "workerContainer": u"wcon",
        "workerMachineType": u"mty",
        "workerCommand": u"wcom",
        "workerCount": 2,
        "parameterServerContainer": u"pscon",
        "parameterServerMachineType": u"psmtype",
        "parameterServerCommand": u"ls",
        "parameterServerCount": 2,
        "workerContainerUser": u"usr",
        "workerRegistryUsername": u"rusr",
        "workerRegistryPassword": u"rpass",
        "parameterServerContainerUser": u"pscuser",
        "parameterServerRegistryContainerUser": u"psrcus",
        "parameterServerRegistryPassword": u"psrpass",
    }
    RESPONSE_JSON_200 = {"handle": "sadkfhlskdjh", "message": "success"}
    RESPONSE_CONTENT_200 = b'{"handle":"sadkfhlskdjh","message":"success"}\n'
    EXPECTED_STDOUT = "New experiment created with handle: sadkfhlskdjh\n"

    @mock.patch("paperspace.cli.commands.client.requests.post")
    def test_should_send_proper_data_and_print_message_when_create_experiment_was_run_with_basic_options(self,
                                                                                                         post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200, 200, self.RESPONSE_CONTENT_200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.BASIC_OPTIONS_COMMAND)

        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS,
                                             json=self.BASIC_OPTIONS_REQUEST,
                                             params=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.cli.commands.client.requests.post")
    def test_should_send_proper_data_and_print_message_when_create_experiment_was_run_with_full_options(self,
                                                                                                        post_patched):
        post_patched.return_value = MockResponse(self.RESPONSE_JSON_200, 200, self.RESPONSE_CONTENT_200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.FULL_OPTIONS_COMMAND)

        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS,
                                             json=self.FULL_OPTIONS_REQUEST,
                                             params=None)
        assert result.output == self.EXPECTED_STDOUT
        assert result.exit_code == 0


class TestExperimentsCreateAndStartSingleNode(TestExperimentsCreateSingleNode):
    URL = "https://services.paperspace.io/experiments/v1/experiments/create_and_start/"
    BASIC_OPTIONS_COMMAND = [
        "experiments", "createAndStart", "singlenode",
        "--name", "exp1",
        "--projectHandle", "testHandle",
        "--container", "testContainer",
        "--machineType", "testType",
        "--command", "testCommand",
        "--workspaceUrl", "some-workspace",
    ]
    FULL_OPTIONS_COMMAND = [
        "experiments", "createAndStart", "singlenode",
        "--name", "exp1",
        "--ports", 4567,
        "--workspaceUrl", "wsp.url",
        "--workingDirectory", "/work/dir/",
        "--artifactDirectory", "/artifact/dir/",
        "--clusterId", 42,
        "--experimentEnv", '{"key":"val"}',
        "--triggerEventId", 45678,
        "--projectId", 987654,
        "--projectHandle", "testHandle",
        "--container", "testContainer",
        "--machineType", "testType",
        "--command", "testCommand",
        "--count", 2,
        "--containerUser", "conUser",
        "--registryUsername", "userName",
        "--registryPassword", "passwd",
    ]
    EXPECTED_STDOUT = "New experiment created and started with handle: sadkfhlskdjh\n"


class TestExperimentsCreateAndStartMultiNode(TestExperimentsCreateMultiNode):
    URL = "https://services.paperspace.io/experiments/v1/experiments/create_and_start/"
    BASIC_OPTIONS_COMMAND = [
        "experiments", "createAndStart", "multinode",
        "--name", "multinode_mpi",
        "--projectHandle", "prq70zy79",
        "--experimentTypeId", "GRPC",
        "--workerContainer", "wcon",
        "--workerMachineType", "mty",
        "--workerCommand", "wcom",
        "--workerCount", 2,
        "--parameterServerContainer", "pscon",
        "--parameterServerMachineType", "psmtype",
        "--parameterServerCommand", "ls",
        "--parameterServerCount", 2,
        "--workerContainerUser", "usr",
        "--workspaceUrl", "some-workspace",
    ]
    FULL_OPTIONS_COMMAND = [
        "experiments", "createAndStart", "multinode",
        "--name", "multinode_mpi",
        "--ports", 3456,
        "--workspaceUrl", "wurl",
        "--workingDirectory", "/dir",
        "--artifactDirectory", "/artdir",
        "--clusterId", 2,
        "--experimentEnv", '{"key":"val"}',
        "--triggerEventId", 12,
        "--projectId", 34,
        "--projectHandle", "prq70zy79",
        "--experimentTypeId", "MPI",
        "--workerContainer", "wcon",
        "--workerMachineType", "mty",
        "--workerCommand", "wcom",
        "--workerCount", 2,
        "--parameterServerContainer", "pscon",
        "--parameterServerMachineType", "psmtype",
        "--parameterServerCommand", "ls",
        "--parameterServerCount", 2,
        "--workerContainerUser", "usr",
        "--workerRegistryUsername", "rusr",
        "--workerRegistryPassword", "rpass",
        "--parameterServerContainerUser", "pscuser",
        "--parameterServerRegistryContainerUser", "psrcus",
        "--parameterServerRegistryPassword", "psrpass",
    ]
    EXPECTED_STDOUT = "New experiment created and started with handle: sadkfhlskdjh\n"


class TestExperimentDetail(object):
    COMMAND = ["experiments", "details", "experiment-id"]
    DETAILS_JSON = {
        "data": {
            "dtCreated": "2019-03-20T19:56:50.154853+00:00",
            "dtDeleted": None,
            "dtFinished": None,
            "dtModified": "2019-03-20T19:56:50.154853+00:00",
            "dtProvisioningFinished": None,
            "dtProvisioningStarted": None,
            "dtStarted": None,
            "dtTeardownFinished": None,
            "dtTeardownStarted": None,
            "experimentError": None,
            "experimentTemplateHistoryId": 6297,
            "experimentTemplateId": 60,
            "experimentTypeId": 3,
            "handle": "ew69ls0vy3eto",
            "id": 6286,
            "projectHandle": "prq70zy79",
            "projectId": 612,
            "started_by_user_id": 1,
            "state": 1,
            "templateHistory": {
                "dtCreated": "2019-03-20T19:56:49.427354+00:00",
                "dtDeleted": None,
                "experimentTemplateId": 60,
                "id": 6297,
                "params": {
                    "artifactDirectory": "/artdir",
                    "clusterId": 2,
                    "experimentEnv": {
                        "key": "val"
                    },
                    "experimentTypeId": 3,
                    "name": "multinode_mpi",
                    "parameter_server_command": "ls",
                    "parameter_server_container": "pscon",
                    "parameter_server_container_user": "pscuser",
                    "parameter_server_count": 2,
                    "parameter_server_machine_type": "psmtype",
                    "parameter_server_registry_password": "psrpass",
                    "parameter_server_registry_username": "psrcus",
                    "ports": 3456,
                    "project_handle": "prq70zy79",
                    "project_id": 34,
                    "trigger_event_id": 12,
                    "worker_command": "wcom",
                    "worker_container": "wcon",
                    "worker_container_user": "usr",
                    "worker_count": 2,
                    "worker_machine_type": "mty",
                    "worker_registry_password": "rpass",
                    "worker_registry_username": "rusr",
                    "workingDirectory": "/dir",
                    "workspaceUrl": "wurl"
                },
                "triggerEvent": {
                    "dtCreated": "2019-03-11T14:47:57+00:00",
                    "eventData": {
                        "author": {
                            "email": "bluckey@paperspace.com",
                            "login": "ultrabluewolf",
                            "name": "Britney Luckey"
                        },
                        "branch": "feature/test-1",
                        "message": "Update readme #2",
                        "repo_node_id": "MDEwOlJlcG9zaXRvcnkxNzQ3MjI3NDc=",
                        "sender": {
                            "id": 4633049,
                            "login": "ultrabluewolf"
                        },
                        "sha": "daa117a00cd1e0e9b1b55695031e698a560cca29",
                        "timestamp": "2019-03-11T10:47:57-04:00"
                    },
                    "id": 12,
                    "type": "github"
                },
                "triggerEventId": 12
            }
        },
        "message": "success"
    }
    DETAILS_STDOUT = """+-------------------------------+----------------+
| Name                          | multinode_mpi  |
+-------------------------------+----------------+
| Handle                        | ew69ls0vy3eto  |
| State                         | created        |
| Artifact directory            | /artdir        |
| Cluster ID                    | 2              |
| Experiment Env                | {'key': 'val'} |
| Experiment Type               | MPI multi node |
| Parameter Server Command      | ls             |
| Parameter Server Container    | pscon          |
| Parameter Server Count        | 2              |
| Parameter Server Machine Type | psmtype        |
| Ports                         | 3456           |
| Project Handle                | prq70zy79      |
| Worker Command                | wcom           |
| Worker Container              | wcon           |
| Worker Count                  | 2              |
| Worker Machine Type           | mty            |
| Working Directory             | /dir           |
| Workspace URL                 | wurl           |
+-------------------------------+----------------+
"""

    @mock.patch("paperspace.cli.commands.client.requests.get")
    def test_should_send_get_request_and_print_experiment_details_in_a_table(self, get_patched):
        get_patched.return_value = MockResponse(self.DETAILS_JSON, 200, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.DETAILS_STDOUT
        assert result.exit_code == 0

    @mock.patch("paperspace.cli.commands.client.requests.get")
    def test_should_send_get_request_and_print_request_content_when_response_data_was_malformed(self, get_patched):
        get_patched.return_value = MockResponse({}, 200, "fake content")
        g = """Error parsing response data
fake content
"""

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == g
        assert result.exit_code == 0


class TestExperimentList(object):
    COMMAND = ["experiments", "list"]
    LIST_JSON = {
        "data": [
            {
                "dtCreated": "2019-03-21T07:47:05.616096+00:00",
                "dtDeleted": None,
                "dtFinished": None,
                "dtModified": "2019-03-21T07:47:05.616096+00:00",
                "dtProvisioningFinished": None,
                "dtProvisioningStarted": None,
                "dtStarted": None,
                "dtTeardownFinished": None,
                "dtTeardownStarted": None,
                "experimentError": None,
                "experimentTemplateHistoryId": 6315,
                "experimentTemplateId": 60,
                "experimentTypeId": 1,
                "handle": "ea2lfbbpdyzsq",
                "id": 6292,
                "projectHandle": "prq70zy79",
                "projectId": 612,
                "started_by_user_id": 1,
                "state": 1,
                "templateHistory": {
                    "dtCreated": "2019-03-21T07:47:04.925852+00:00",
                    "dtDeleted": None,
                    "experimentTemplateId": 60,
                    "id": 6315,
                    "params": {
                        "experimentTypeId": 1,
                        "name": "dsfads",
                        "ports": 5000,
                        "project_handle": "prq70zy79",
                        "worker_command": "sadas",
                        "worker_container": "asd",
                        "worker_machine_type": "sadas"
                    },
                    "triggerEvent": None,
                    "triggerEventId": None
                }
            },
            {
                "dtCreated": "2019-03-21T07:46:57.706055+00:00",
                "dtDeleted": None,
                "dtFinished": None,
                "dtModified": "2019-03-21T07:46:57.706055+00:00",
                "dtProvisioningFinished": None,
                "dtProvisioningStarted": None,
                "dtStarted": None,
                "dtTeardownFinished": None,
                "dtTeardownStarted": None,
                "experimentError": None,
                "experimentTemplateHistoryId": 6314,
                "experimentTemplateId": 60,
                "experimentTypeId": 1,
                "handle": "em6btk2vtb7it",
                "id": 6291,
                "projectHandle": "prq70zy79",
                "projectId": 612,
                "started_by_user_id": 1,
                "state": 1,
                "templateHistory": {
                    "dtCreated": "2019-03-21T07:46:56.949590+00:00",
                    "dtDeleted": None,
                    "experimentTemplateId": 60,
                    "id": 6314,
                    "params": {
                        "experimentTypeId": 1,
                        "name": "dsfads",
                        "ports": 5000,
                        "project_handle": "prq70zy79",
                        "worker_command": "sadas",
                        "worker_container": "asd",
                        "worker_machine_type": "sadas"
                    },
                    "triggerEvent": None,
                    "triggerEventId": None
                }
            },
            {
                "dtCreated": "2019-03-20T19:56:50.154853+00:00",
                "dtDeleted": None,
                "dtFinished": None,
                "dtModified": "2019-03-20T19:56:50.154853+00:00",
                "dtProvisioningFinished": None,
                "dtProvisioningStarted": None,
                "dtStarted": None,
                "dtTeardownFinished": None,
                "dtTeardownStarted": None,
                "experimentError": None,
                "experimentTemplateHistoryId": 6297,
                "experimentTemplateId": 60,
                "experimentTypeId": 3,
                "handle": "ew69ls0vy3eto",
                "id": 6286,
                "projectHandle": "prq70zy79",
                "projectId": 612,
                "started_by_user_id": 1,
                "state": 1,
                "templateHistory": {
                    "dtCreated": "2019-03-20T19:56:49.427354+00:00",
                    "dtDeleted": None,
                    "experimentTemplateId": 60,
                    "id": 6297,
                    "params": {
                        "artifactDirectory": "/artdir",
                        "clusterId": 2,
                        "experimentEnv": {
                            "key": "val"
                        },
                        "experimentTypeId": 3,
                        "name": "multinode_mpi",
                        "parameter_server_command": "ls",
                        "parameter_server_container": "pscon",
                        "parameter_server_container_user": "pscuser",
                        "parameter_server_count": 2,
                        "parameter_server_machine_type": "psmtype",
                        "parameter_server_registry_password": "psrpass",
                        "parameter_server_registry_username": "psrcus",
                        "ports": 3456,
                        "project_handle": "prq70zy79",
                        "project_id": 34,
                        "trigger_event_id": 12,
                        "worker_command": "wcom",
                        "worker_container": "wcon",
                        "worker_container_user": "usr",
                        "worker_count": 2,
                        "worker_machine_type": "mty",
                        "worker_registry_password": "rpass",
                        "worker_registry_username": "rusr",
                        "workingDirectory": "/dir",
                        "workspaceUrl": "wurl"
                    },
                    "triggerEvent": {
                        "dtCreated": "2019-03-11T14:47:57+00:00",
                        "eventData": {
                            "author": {
                                "email": "bluckey@paperspace.com",
                                "login": "ultrabluewolf",
                                "name": "Britney Luckey"
                            },
                            "branch": "feature/test-1",
                            "message": "Update readme #2",
                            "repo_node_id": "MDEwOlJlcG9zaXRvcnkxNzQ3MjI3NDc=",
                            "sender": {
                                "id": 4633049,
                                "login": "ultrabluewolf"
                            },
                            "sha": "daa117a00cd1e0e9b1b55695031e698a560cca29",
                            "timestamp": "2019-03-11T10:47:57-04:00"
                        },
                        "id": 12,
                        "type": "github"
                    },
                    "triggerEventId": 12
                }
            }
        ],
        "message": "success",
        "meta": {
            "filter": [],
            "limit": 11,
            "offset": 0,
            "totalItems": 27
        }
    }
    DETAILS_STDOUT = """+---------------+---------------+---------+
| Name          | Handle        | Status  |
+---------------+---------------+---------+
| dsfads        | ea2lfbbpdyzsq | created |
| dsfads        | em6btk2vtb7it | created |
| multinode_mpi | ew69ls0vy3eto | created |
+---------------+---------------+---------+
"""

    @mock.patch("paperspace.cli.commands.client.requests.get")
    def test_should_send_get_request_and_print_list_of_experiments(self, get_patched):
        get_patched.return_value = MockResponse(self.LIST_JSON, 200, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.DETAILS_STDOUT


class TestStartExperiment(object):
    COMMAND = ["experiments", "start", "some-handle"]
    RESPONSE_JSON = {"message": "success"}
    START_STDOUT = "Experiment started\n"

    @mock.patch("paperspace.cli.commands.client.requests.put")
    def test_should_send_put_request_and_print_confirmation(self, put_patched):
        put_patched.return_value = MockResponse(self.RESPONSE_JSON, 200, "fake content")

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.START_STDOUT

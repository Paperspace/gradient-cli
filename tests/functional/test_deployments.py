import mock
import json
from click.testing import CliRunner

from gradient.api_sdk.clients import http_client
from gradient.cli import cli

EXPECTED_HEADERS = http_client.default_headers.copy()
EXPECTED_HEADERS["ps_client_name"] = "gradient-cli"

EXPECTED_HEADERS_WITH_CHANGED_API_KEY = EXPECTED_HEADERS.copy()
EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"

URL = "https://api.paperspace.io"


class TestCreateDeployments(object):
    LOAD_SPEC_VALUE = {
        "image": "lucone83/streamlit-nginx",
        "port": 8080,
        "resources": {
            "replicas": 1,
            "instanceType": "C4"
        }
    }

    @mock.patch("gradient.cli.gradient_deployments.load_spec", return_value=LOAD_SPEC_VALUE)
    @mock.patch("gradient.api_sdk.repositories.gradient_deployments.create_deployment")
    def test_create_deployments(self, method, load_spec):
        STDOUT = "Created deployment: 5c229375-6f77-41b1-afbc-acd00cac9b77"
        method.return_value = {"id": "5c229375-6f77-41b1-afbc-acd00cac9b77"}

        result = CliRunner().invoke(
            cli.cli,
            ["deployments", "create"] + [
                "--name=test-deployment",
                "--projectId=prsmlkp15",
                "--spec=./deployment.yaml",
                "--apiKey=some_key"
            ]
        )

        assert STDOUT in result.output


class TestUpdateDeployments(object):
    LOAD_SPEC_VALUE = {
        "image": "lucone83/streamlit-nginx",
        "port": 8080,
        "resources": {
            "replicas": 1,
            "instanceType": "C4"
        }
    }

    @mock.patch("gradient.cli.gradient_deployments.load_spec", return_value=LOAD_SPEC_VALUE)
    @mock.patch("gradient.api_sdk.repositories.gradient_deployments.update_deployment")
    def test_update_deployments(self, method, load_spec):
        STDOUT = "Updated deployment: 5c229375-6f77-41b1-afbc-acd00cac9b77"
        method.return_value = {"id": "5c229375-6f77-41b1-afbc-acd00cac9b77"}

        result = CliRunner().invoke(
            cli.cli,
            ["deployments", "update"] + [
                "--id=5c229375-6f77-41b1-afbc-acd00cac9b77"
                "--name=test-deployment",
                "--projectId=prsmlkp15",
                "--spec=./deployment.yaml",
                "--clusterId=cluster_id_1",
                "--apiKey=some_key"]
        )

        assert STDOUT in result.output


class TestListDeployments(object):
    @mock.patch("gradient.api_sdk.repositories.gradient_deployments.list_deployments")
    def test_list_deployments(self, method):
        STDOUT = """+-----------------+--------------------------------------+
| Name            | ID                                   |
+-----------------+--------------------------------------+
| test-fV3opaPJHl | 58dac4ff-fd7c-4da0-97a7-f114c304b3eb |
+-----------------+--------------------------------------+
"""

        method.return_value = [
            {
                "id": "58dac4ff-fd7c-4da0-97a7-f114c304b3eb",
                "name": "test-fV3opaPJHl",
                "deploymentSpecs": {
                    "nodes": [
                        {
                            "id": "efe770ee-6f9d-42cb-b802-66e6dd5d646c",
                            "data": {
                                "image": "bash:5",
                                "port": 8000,
                                "resources": {
                                    "instanceType": "C10",
                                    "replicas": 1
                                }
                            },
                            "endpointUrl": "hash.cluster.paperspacegradient.com",
                            "actor": {
                                "avatarUrl": None,
                                "fullName": None
                            },
                            "deploymentRuns": {
                                "nodes": []
                            }
                        }
                    ]
                }
            }
        ]

        result = CliRunner().invoke(cli.cli, ["deployments", "list", "--apiKey=some_key"])

        assert STDOUT in result.output

    @mock.patch("gradient.api_sdk.repositories.gradient_deployments.list_deployments")
    def test_list_deployments_no_nodes(self, method):
        STDOUT = "No deployments found"

        method.return_value = []

        result = CliRunner().invoke(cli.cli, ["deployments", "list", "--apiKey=some_key"])

        assert STDOUT in result.output


class TestGetDeployment(object):
    @mock.patch("gradient.api_sdk.repositories.gradient_deployments.get_deployment")
    def test_list_deployments(self, method):
        STDOUT = """{
    "id": "efe770ee-6f9d-42cb-b802-66e6dd5d646c",
    "name": "test-deployment-2",
    "deploymentSpecs": [
        {
            "id": "03fe1b5c-e82c-42fe-9f48-4020939aaa58",
            "data": {
                "image": "lucone83/streamlit-nginx",
                "port": 8080,
                "resources": {
                    "instanceType": "Air",
                    "replicas": 1
                },
                "command": null,
                "env": [
                    {
                        "name": "ENV",
                        "value": "VAR"
                    }
                ],
                "models": null
            },
            "endpointUrl": "d5c2293756f7741b1afbcacd00cac9b77.null",
            "actor": {
                "avatarUrl": null,
                "fullName": null
            },
            "cluster": {
                "id": "cl9tz9no4"
            },
            "deploymentRuns": []
        }
    ]
}
"""

        method.return_value = {
            "deployment": {
                "id": "efe770ee-6f9d-42cb-b802-66e6dd5d646c",
                "name": "test-deployment-2",
                "deploymentSpecs": {
                    "nodes": [
                        {
                            "id": "03fe1b5c-e82c-42fe-9f48-4020939aaa58",
                            "data": {
                                "image": "lucone83/streamlit-nginx",
                                "port": 8080,
                                "resources": {
                                    "instanceType": "Air",
                                    "replicas": 1
                                },
                                "command": None,
                                "env": [
                                    {
                                        "name": "ENV",
                                        "value": "VAR"
                                    }
                                ],
                                "models": None
                            },
                            "endpointUrl": "d5c2293756f7741b1afbcacd00cac9b77.null",
                            "actor": {
                                "avatarUrl": None,
                                "fullName": None
                            },
                            "cluster": {
                                "id": "cl9tz9no4"
                            },
                            "deploymentRuns": {
                                "nodes": []
                            }
                        }
                    ]
                }
            }
        }

        result = CliRunner().invoke(
            cli.cli, ["deployments", "get", "--id=efe770ee-6f9d-42cb-b802-66e6dd5d646c", "--apiKey=some_key"])

        assert json.loads(STDOUT) == json.loads(result.output)

    @mock.patch("gradient.api_sdk.repositories.gradient_deployments.get_deployment")
    def test_get_deployment_no_deployment(self, method):
        STDOUT = "Deployment not found"

        method.return_value = {
            "deployment": None
        }

        result = CliRunner().invoke(
            cli.cli, ["deployments", "get", "--id=efe770ee-6f9d-42cb-b802-66e6dd5d646c", "--apiKey=some_key"])

        assert STDOUT in result.output


class TestDeleteDeployment(object):
    @mock.patch("gradient.api_sdk.repositories.gradient_deployments.delete_deployment")
    def test_delete_deployments(self, method):
        STDOUT = "Deleted deployment: 5c229375-6f77-41b1-afbc-acd00cac9b77"

        method.return_value = {
            "deployment": {
                "id": "5c229375-6f77-41b1-afbc-acd00cac9b77"
            }
        }

        result = CliRunner().invoke(
            cli.cli, ["deployments", "delete", "--id=5c229375-6f77-41b1-afbc-acd00cac9b77"])

        assert STDOUT in result.output

    @mock.patch("gradient.api_sdk.repositories.gradient_deployments.delete_deployment")
    def test_delete_deployment_no_deployment(self, method):
        STDOUT = "Deployment not found"

        method.return_value = None

        result = CliRunner().invoke(
            cli.cli, ["deployments", "delete", "--id=5c229375-6f77-41b1-afbc-acd00cac9b78", "--apiKey=some_key"])

        assert STDOUT in result.output

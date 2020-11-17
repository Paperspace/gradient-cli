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


class TestListDatasets(object):
    COMMAND = ["datasets", "list"]

    JSON = example_responses.LIST_DATASETS_RESPONSE

    STDOUT = """+-------+-----------------+-------------------------+
| Name  | ID              | Storage Provider        |
+-------+-----------------+-------------------------+
| test1 | dsttn2y7j1ux882 | test1 (spltautet072md4) |
+-------+-----------------+-------------------------+
"""

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_list_datasets(self, method):
        method.return_value = MockResponse(self.JSON)

        result = CliRunner().invoke(cli.cli, self.COMMAND)

        assert self.STDOUT in result.output, result.exc_info
        method.assert_called_once_with(
            URL + "/datasets",
            headers=EXPECTED_HEADERS,
            json=None,
            params={
                "filter[limit]": 21,
                "filter[skip]": 0,
                "filter[order][]": "name ASC",
            }
        )


class TestShowDatasetDetails(object):
    COMMAND = ["datasets", "details"]

    JSON = example_responses.SHOW_DATASET_DETAILS_RESPONSE

    STDOUT = """+-----------------+-------------------------+
| Name            | test1                   |
+-----------------+-------------------------+
| ID              | dsttn2y7j1ux882         |
| Description     |                         |
| StorageProvider | test1 (spltautet072md4) |
+-----------------+-------------------------+
"""

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_show_dataset_details(self, method):
        method.return_value = MockResponse(self.JSON)

        result = CliRunner().invoke(cli.cli, self.COMMAND + ["--id=dsttn2y7j1ux882"])

        assert self.STDOUT in result.output, result.exc_info
        method.assert_called_once_with(
            URL + "/datasets/dsttn2y7j1ux882",
            headers=EXPECTED_HEADERS,
            json=None,
            params=None
        )


class TestCreateDataset(object):
    COMMAND = ["datasets", "create"]

    JSON = example_responses.CREATE_DATASET_RESPONSE

    STDOUT = """Created dataset: dsttn2y7j1ux882
"""

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_create_dataset(self, method):
        method.return_value = MockResponse(self.JSON)

        result = CliRunner().invoke(cli.cli, self.COMMAND + [
            "--name=test1", "--storageProviderId=spltautet072md4"])

        assert self.STDOUT in result.output, result.exc_info
        method.assert_called_once_with(
            URL + "/datasets",
            json={"name": "test1", "storageProviderId": "spltautet072md4"},
            params=None,
            headers=EXPECTED_HEADERS,
            files=None,
            data=None
        )


class TestUpdateDataset(object):
    COMMAND = ["datasets", "update"]

    JSON = example_responses.UPDATE_DATASET_RESPONSE

    STDOUT = """Updated dataset: dsttn2y7j1ux882
"""

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_update_dataset(self, method):
        method.return_value = MockResponse(self.JSON)

        result = CliRunner().invoke(cli.cli, self.COMMAND + [
            "--id=dsttn2y7j1ux882", "--description=Test dataset"])

        assert self.STDOUT in result.output, result.exc_info
        method.assert_called_once_with(
            URL + "/datasets/dsttn2y7j1ux882",
            json={"description": "Test dataset"},
            params=None,
            headers=EXPECTED_HEADERS,
            files=None,
            data=None
        )


class TestDeleteDataset(object):
    COMMAND = ["datasets", "delete"]

    STDOUT = """Deleted dataset: dsttn2y7j1ux882
"""

    @mock.patch("gradient.api_sdk.clients.http_client.requests.delete")
    def test_delete_dataset(self, method):
        method.return_value = MockResponse(status_code=204)

        result = CliRunner().invoke(cli.cli, self.COMMAND + ["--id=dsttn2y7j1ux882"])

        assert self.STDOUT in result.output, result.exc_info
        method.assert_called_once_with(
            URL + "/datasets/dsttn2y7j1ux882",
            params=None,
            headers=EXPECTED_HEADERS,
            json=None
        )


class TestListDatasetVersions(object):
    COMMAND = ["datasets", "versions", "list"]

    JSON = example_responses.LIST_DATASET_VERSIONS_RESPONSE

    STDOUT = """+-------------------------+---------+-------+
| ID                      | Message | Tags  |
+-------------------------+---------+-------+
| dsttn2y7j1ux882:1rn19s2 |         | hello |
+-------------------------+---------+-------+
"""

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_list_dataset_versions(self, method):
        method.return_value = MockResponse(self.JSON)

        result = CliRunner().invoke(cli.cli, self.COMMAND + ["--id=dsttn2y7j1ux882"])

        assert self.STDOUT in result.output, result.exc_info
        method.assert_called_once_with(
            URL + "/datasets/dsttn2y7j1ux882/versions",
            headers=EXPECTED_HEADERS,
            json=None,
            params={
                "filter[limit]": 21,
                "filter[skip]": 0,
                "filter[where][isCommitted]": "true",
                "filter[order][]": "dtCreated DESC",
            }
        )


class TestShowDatasetVersionDetails(object):
    COMMAND = ["datasets", "versions", "details"]

    JSON = example_responses.SHOW_DATASET_VERSION_DETAILS_RESPONSE

    STDOUT = """+-----------+-------------------------+
| ID        | dsttn2y7j1ux882:1rn19s2 |
+-----------+-------------------------+
| Message   |                         |
| Committed | true                    |
| Tags      | hello                   |
+-----------+-------------------------+
"""

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_show_dataset_details(self, method):
        method.return_value = MockResponse(self.JSON)

        result = CliRunner().invoke(cli.cli, self.COMMAND + ["--id=dsttn2y7j1ux882:1rn19s2"])

        assert self.STDOUT in result.output, result.exc_info
        method.assert_called_once_with(
            URL + "/datasets/dsttn2y7j1ux882/versions/1rn19s2",
            headers=EXPECTED_HEADERS,
            json=None,
            params=None
        )


class TestUpdateDatasetVersion(object):
    COMMAND = ["datasets", "versions", "update"]

    JSON = example_responses.UPDATE_DATASET_VERSION_RESPONSE

    STDOUT = """Updated dataset version: dsttn2y7j1ux882:1rn19s2
"""

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_update_dataset_version(self, method):
        method.return_value = MockResponse(self.JSON)

        result = CliRunner().invoke(cli.cli, self.COMMAND + [
            "--id=dsttn2y7j1ux882:1rn19s2", "--message=Test message"])

        assert self.STDOUT in result.output, result.exc_info
        method.assert_called_once_with(
            URL + "/datasets/dsttn2y7j1ux882/versions/1rn19s2",
            json={"message": "Test message"},
            params=None,
            headers=EXPECTED_HEADERS,
            files=None,
            data=None
        )


class TestDeleteDatasetVersion(object):
    COMMAND = ["datasets", "versions", "delete"]

    STDOUT = """Deleted dataset version: dsttn2y7j1ux882:1rn19s2
"""

    @mock.patch("gradient.api_sdk.clients.http_client.requests.delete")
    def test_delete_dataset_version(self, method):
        method.return_value = MockResponse(status_code=204)

        result = CliRunner().invoke(cli.cli, self.COMMAND + ["--id=dsttn2y7j1ux882:1rn19s2"])

        assert self.STDOUT in result.output, result.exc_info
        method.assert_called_once_with(
            URL + "/datasets/dsttn2y7j1ux882/versions/1rn19s2",
            params=None,
            headers=EXPECTED_HEADERS,
            json=None
        )


class TestSetDatasetTag(object):
    COMMAND = ["datasets", "tags", "set"]

    JSON = example_responses.SET_DATASET_VERSION_TAG_RESPONSE

    STDOUT = """Set dataset tag: dsttn2y7j1ux882:hello
"""

    @mock.patch("gradient.api_sdk.clients.http_client.requests.put")
    def test_update_dataset_version(self, method):
        method.return_value = MockResponse(self.JSON)

        result = CliRunner().invoke(cli.cli, self.COMMAND + [
            "--id=dsttn2y7j1ux882:1rn19s2", "--name=hello"])

        assert self.STDOUT in result.output, result.exc_info
        method.assert_called_once_with(
            URL + "/datasets/dsttn2y7j1ux882/tags/hello",
            json={"version": "1rn19s2"},
            params=None,
            headers=EXPECTED_HEADERS,
            data=None
        )


class TestDeleteDatasetTag(object):
    COMMAND = ["datasets", "tags", "delete"]

    STDOUT = """Deleted dataset tag: dsttn2y7j1ux882:hello
"""

    @mock.patch("gradient.api_sdk.clients.http_client.requests.delete")
    def test_update_dataset_version(self, method):
        method.return_value = MockResponse()

        result = CliRunner().invoke(cli.cli, self.COMMAND + [
            "--id=dsttn2y7j1ux882:hello"])

        assert self.STDOUT in result.output, result.exc_info
        method.assert_called_once_with(
            URL + "/datasets/dsttn2y7j1ux882/tags/hello",
            params=None,
            headers=EXPECTED_HEADERS,
            json=None
        )

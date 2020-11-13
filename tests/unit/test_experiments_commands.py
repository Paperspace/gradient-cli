import pytest
from click import BadParameter

from gradient.commands.experiments import BaseCreateExperimentCommandMixin


class TestHandleDatasetDataMethod(object):
    def test_should_transform_lists_of_datasets_parameters_to_list_of_dicts_and_leave_other_data_intact(self):
        input_data = {
            "some_key": "some_value",
            "dataset_uri_list": ["uri1", "uri2"],
            "dataset_id_list": [None, None, "test"],
            "dataset_name_list": ["name1", None, "name2"],
            "dataset_access_key_id_list": [None, "key_id"],
            "dataset_secret_access_key_list": ["none", "secret"],
            # "dataset_version_id_list": []  # this key does not exist if parameter was not used
            "dataset_etag_list": ["etag"],
            "dataset_volume_kind_list": [],
        }
        expected_data = {
            "some_key": "some_value",
            "datasets": [
                {
                    "uri": "uri1",
                    "id": None,
                    "name": "name1",
                    "aws_access_key_id": None,
                    "aws_secret_access_key": None,
                    "aws_endpoint": None,
                    "version_id": None,
                    "etag": "etag",
                    "volume_kind": None,
                    "volume_size": None,
                },
                {
                    "uri": "uri2",
                    "id": None,
                    "name": None,
                    "aws_access_key_id": "key_id",
                    "aws_secret_access_key": "secret",
                    "aws_endpoint": None,
                    "version_id": None,
                    "etag": None,
                    "volume_kind": None,
                    "volume_size": None,
                },
                {
                    "uri": None,
                    "id": "test",
                    "name": "name2",
                    "aws_access_key_id": None,
                    "aws_secret_access_key": None,
                    "aws_endpoint": None,
                    "version_id": None,
                    "etag": None,
                    "volume_kind": None,
                    "volume_size": None,
                },
            ]

        }

        BaseCreateExperimentCommandMixin._handle_dataset_data(input_data)

        assert expected_data == input_data

    def test_should_raise_exception_if_number_of_any_dataset_parameter_is_greater_than_number_of_dataset_uris(self):
        input_data = {
            "some_key": "some_value",
            "dataset_uri_list": ["uri1", "uri2"],
            "dataset_name_list": ["name1", None],
            "dataset_access_key_id_list": [None, "key_id"],
            "dataset_secret_access_key_list": ["none", "secret"],
            # "dataset_version_id_list": []  # this key does not exist if parameter was not used
            "dataset_etag_list": ["etag", "etag2", "etag3"],  # more etags than uris
        }

        with pytest.raises(BadParameter):
            BaseCreateExperimentCommandMixin._handle_dataset_data(input_data)

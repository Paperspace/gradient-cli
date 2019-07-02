import abc

import six

from gradient import constants
from gradient.api_sdk import exceptions, serializers
from gradient.utils import MessageExtractor
from gradient.workspace import S3WorkspaceHandler
from .base_client import BaseClient
from ..clients import http_client
from ..exceptions import GradientSdkError
from ..models import SingleNodeExperiment, MultiNodeExperiment
from ..serializers import SingleNodeExperimentSchema, MultiNodeExperimentSchema


class ExperimentsClient(BaseClient):
    def create_single_node(self, name, project_id, machine_type, command, ports=None, workspace=None,
                           workspace_archive=None, workspace_url=None, ignore_files=None, working_directory=None,
                           artifact_directory=None, cluster_id=None, experiment_env=None, model_type=None,
                           model_path=None, container=None, container_user=None, registry_username=None,
                           registry_password=None):
        """Create single node experiment

        :param str name:
        :param str project_id:
        :param str machine_type:
        :param str command:
        :param str ports:
        :param str workspace:
        :param str workspace_archive:
        :param str workspace_url:
        :param list[str] ignore_files:
        :param str working_directory:
        :param str artifact_directory:
        :param str cluster_id:
        :param dict experiment_env:
        :param str model_type:
        :param str model_path:
        :param str container:
        :param str container_user:
        :param str registry_username:
        :param str registry_password:

        :rtype: str
        """

        if ignore_files is None:
            ignore_files = []

        experiment = SingleNodeExperiment(experiment_type_id=constants.ExperimentType.SINGLE_NODE, name=name,
                                          project_id=project_id, machine_type=machine_type, ports=ports,
                                          workspace=workspace, workspace_archive=workspace_archive,
                                          workspace_url=workspace_url, ignore_files=ignore_files,
                                          working_directory=working_directory, artifact_directory=artifact_directory,
                                          cluster_id=cluster_id, experiment_env=experiment_env, model_type=model_type,
                                          model_path=model_path, container=container, command=command,
                                          container_user=container_user, registry_username=registry_username,
                                          registry_password=registry_password)

        handle = self._create(experiment, SingleNodeExperimentSchema)
        return handle

    def create_multi_node(self, name, project_id, experiment_type_id, worker_container, worker_machine_type,
                          worker_command, worker_count, parameter_server_container, parameter_server_machine_type,
                          parameter_server_command, parameter_server_count, ports=None, workspace=None,
                          workspace_archive=None, workspace_url=None, ignore_files=None, working_directory=None,
                          artifact_directory=None, cluster_id=None, experiment_env=None, model_type=None,
                          model_path=None, worker_container_user=None, worker_registry_username=None,
                          worker_registry_password=None, parameter_server_container_user=None,
                          parameter_server_registry_container_user=None, parameter_server_registry_password=None):

        experiment = MultiNodeExperiment(name=name, project_id=project_id, experiment_type_id=experiment_type_id,
                                         worker_container=worker_container, worker_machine_type=worker_machine_type,
                                         worker_command=worker_command, worker_count=worker_count,
                                         parameter_server_container=parameter_server_container,
                                         parameter_server_machine_type=parameter_server_machine_type,
                                         parameter_server_command=parameter_server_command,
                                         parameter_server_count=parameter_server_count, ports=ports,
                                         workspace=workspace,
                                         workspace_archive=workspace_archive, workspace_url=workspace_url,
                                         ignore_files=ignore_files,
                                         working_directory=working_directory,
                                         artifact_directory=artifact_directory, cluster_id=cluster_id,
                                         experiment_env=experiment_env,
                                         model_type=model_type, model_path=model_path,
                                         worker_container_user=worker_container_user,
                                         worker_registry_username=worker_registry_username,
                                         worker_registry_password=worker_registry_password,
                                         parameter_server_container_user=parameter_server_container_user,
                                         parameter_server_registry_container_user=parameter_server_registry_container_user,
                                         parameter_server_registry_password=parameter_server_registry_password)

        handle = self._create(experiment, MultiNodeExperimentSchema)
        return handle

    def run_single_node(self, name, project_id, machine_type, command, ports=None, workspace=None,
                        workspace_archive=None, workspace_url=None, ignore_files=None, working_directory=None,
                        artifact_directory=None, cluster_id=None, experiment_env=None, model_type=None, model_path=None,
                        container=None, container_user=None, registry_username=None, registry_password=None):
        """Create and start single node experiment

        :param str name:
        :param str project_id:
        :param str machine_type:
        :param str command:
        :param str ports:
        :param str workspace:
        :param str workspace_archive:
        :param str workspace_url:
        :param list[str] ignore_files:
        :param str working_directory:
        :param str artifact_directory:
        :param str cluster_id:
        :param dict experiment_env:
        :param str model_type:
        :param str model_path:
        :param str container:
        :param str container_user:
        :param str registry_username:
        :param str registry_password:

        :rtype: str
        """

        experiment = SingleNodeExperiment(experiment_type_id=constants.ExperimentType.SINGLE_NODE, name=name,
                                          project_id=project_id, machine_type=machine_type, ports=ports,
                                          workspace=workspace, workspace_archive=workspace_archive,
                                          workspace_url=workspace_url, ignore_files=ignore_files,
                                          working_directory=working_directory, artifact_directory=artifact_directory,
                                          cluster_id=cluster_id, experiment_env=experiment_env, model_type=model_type,
                                          model_path=model_path, container=container, command=command,
                                          container_user=container_user, registry_username=registry_username,
                                          registry_password=registry_password)

        handle = self._run(experiment, SingleNodeExperimentSchema)
        return handle

    def run_multi_node(self, name, project_id, experiment_type_id, worker_container, worker_machine_type,
                       worker_command, worker_count, parameter_server_container, parameter_server_machine_type,
                       parameter_server_command, parameter_server_count, ports=None, workspace=None,
                       workspace_archive=None, workspace_url=None, ignore_files=None, working_directory=None,
                       artifact_directory=None, cluster_id=None, experiment_env=None,
                       model_type=None, model_path=None, worker_container_user=None, worker_registry_username=None,
                       worker_registry_password=None, parameter_server_container_user=None,
                       parameter_server_registry_container_user=None, parameter_server_registry_password=None):

        experiment = MultiNodeExperiment(name=name, project_id=project_id, experiment_type_id=experiment_type_id,
                                         worker_container=worker_container, worker_machine_type=worker_machine_type,
                                         worker_command=worker_command, worker_count=worker_count,
                                         parameter_server_container=parameter_server_container,
                                         parameter_server_machine_type=parameter_server_machine_type,
                                         parameter_server_command=parameter_server_command,
                                         parameter_server_count=parameter_server_count, ports=ports,
                                         workspace=workspace,
                                         workspace_archive=workspace_archive, workspace_url=workspace_url,
                                         ignore_files=ignore_files,
                                         working_directory=working_directory,
                                         artifact_directory=artifact_directory, cluster_id=cluster_id,
                                         experiment_env=experiment_env,
                                         model_type=model_type, model_path=model_path,
                                         worker_container_user=worker_container_user,
                                         worker_registry_username=worker_registry_username,
                                         worker_registry_password=worker_registry_password,
                                         parameter_server_container_user=parameter_server_container_user,
                                         parameter_server_registry_container_user=parameter_server_registry_container_user,
                                         parameter_server_registry_password=parameter_server_registry_password)

        handle = self._run(experiment, MultiNodeExperimentSchema)
        return handle

    def start(self, experiment_id):
        """Start existing experiment

        :type experiment_id: str
        :rtype: http_client.GradientResponse
        """
        response = self._get_start_response(experiment_id)
        gradient_response = self._interpret_response(response)
        return gradient_response

    def stop(self, experiment_id):
        """Stop running experiment

        :type experiment_id: str
        :rtype: http_client.GradientResponse
        """
        response = self._get_stop_response(experiment_id)
        gradient_response = self._interpret_response(response)
        return gradient_response

    def list(self, project_id=None):
        """Get a list of experiments. Optionally filter by project ID

        :type project_id: str|list|None
        :rtype: list[SingleNodeExperiment|MultiNodeExperiment]
        """
        experiments = ListExperiments(self._client).list(project_id=project_id)
        return experiments

    def _create(self, experiment, schema_cls):
        experiment_dict = self._get_experiment_dict(experiment, schema_cls)
        response = self._get_create_response(experiment_dict)
        handle = self._process_response(response)
        return handle

    @staticmethod
    def _list_to_comma_separated(lst):
        comma_separated_str = ".".join(lst)
        return comma_separated_str

    def _run(self, experiment, schema_cls):
        experiment_dict = self._get_experiment_dict(experiment, schema_cls)
        response = self._get_run_response(experiment_dict)
        handle = self._process_response(response)
        return handle

    def _get_create_response(self, experiment_dict):
        response = self._client.post("/experiments/", json=experiment_dict)
        return response

    def _get_run_response(self, experiment_dict):
        response = self._client.post("/experiments/create_and_start/", json=experiment_dict)
        return response

    def _process_response(self, response):
        if response.ok:
            return response.json()["handle"]

        msg = self._get_error_message(response)
        raise GradientSdkError(msg)

    @staticmethod
    def _get_error_message(response):
        try:
            response_data = response.json()
        except ValueError:
            return "Unknown error"

        msg = MessageExtractor().get_message_from_response_data(response_data)
        return msg

    def _get_experiment_dict(self, experiment, schema_cls):
        experiment_schema = schema_cls()
        experiment_dict = experiment_schema.dump(experiment).data

        workspace_url = self._get_workspace_url(experiment_dict)
        if workspace_url:
            experiment_dict["workspaceUrl"] = workspace_url

        ignore_files = experiment_dict.pop("ignore_files", None)
        if ignore_files:
            experiment_dict["ignore_files"] = self._list_to_comma_separated(ignore_files)

        return experiment_dict

    def _get_workspace_url(self, experiment_dict):
        workspace_handler = S3WorkspaceHandler(experiments_api=self._client, logger_=self.logger)
        workspace_url = workspace_handler.handle(experiment_dict)
        return workspace_url

    @staticmethod
    def _interpret_response(response):
        gradient_response = http_client.GradientResponse.interpret_response(response)
        return gradient_response

    def _get_start_response(self, experiment_id):
        url = "/experiments/{}/start/".format(experiment_id)
        response = self._client.put(url)
        return response

    def _get_stop_response(self, experiment_id):
        url = "/experiments/{}/stop/".format(experiment_id)
        response = self._client.put(url)
        return response


@six.add_metaclass(abc.ABCMeta)
class ListResources(object):
    def __init__(self, api):
        self.api = api

    @abc.abstractproperty
    def request_url(self):
        """
        :rtype: str
        """
        pass

    @abc.abstractmethod
    def _parse_objects(self, data, **kwargs):
        pass

    def list(self, **kwargs):
        response = self._get_response(kwargs)
        self._validate_response(response)
        objects = self._get_objects(response, **kwargs)
        return objects

    def _get_response(self, kwargs):
        json_ = self._get_request_json(kwargs)
        params = self._get_request_params(kwargs)
        response = self.api.get(self.request_url, json=json_, params=params)
        gradient_response = http_client.GradientResponse.interpret_response(response)

        return gradient_response

    @staticmethod
    def _validate_response(response):
        if not response.ok:
            msg = "Failed to fetch data"
            errors = MessageExtractor().get_message_from_response_data(response.data)
            if errors:
                msg += ": " + errors
            raise exceptions.ResourceFetchingError(msg)

    def _get_objects(self, response, **kwargs):
        if not response.data:
            return []

        objects = self._parse_objects(response.data, **kwargs)
        return objects

    def _get_request_json(self, kwargs):
        return None

    def _get_request_params(self, kwargs):
        return None


class ListExperiments(ListResources):
    @property
    def request_url(self):
        return "/experiments/"

    def _parse_objects(self, data, **kwargs):
        experiments_dicts = self._get_experiments_dicts_from_json_data(data, kwargs)
        experiments = []
        for experiment_dict in experiments_dicts:
            experiment_dict.update(experiment_dict["templateHistory"]["params"])

            if self._is_single_node_experiment(experiment_dict):
                experiment = serializers.SingleNodeExperimentSchema().get_instance(experiment_dict)
            else:
                experiment = serializers.MultiNodeExperimentSchema().get_instance(experiment_dict)
            experiments.append(experiment)

        return experiments

    @staticmethod
    def _is_single_node_experiment(experiment_dict):
        return "parameter_server_machine_type" not in experiment_dict["templateHistory"]["params"]

    @staticmethod
    def _get_experiments_dicts_from_json_data(data, kwargs):
        filtered = bool(kwargs.get("project_id"))
        if not filtered:  # If filtering by project ID response data has different format...
            return data["data"]

        experiments = []
        for project_experiments in data["data"]:
            for experiment in project_experiments["data"]:
                experiments.append(experiment)

        return experiments

    def _get_request_params(self, kwargs):
        params = {"limit": -1}  # so the API sends back full list without pagination

        project_id = kwargs.get("project_id")
        if project_id:
            for i, experiment_id in enumerate(project_id):
                key = "projectHandle[{}]".format(i)
                params[key] = experiment_id

        return params

from gradient import constants
from gradient.utils import MessageExtractor
from gradient.workspace import S3WorkspaceHandler
from .base_client import BaseClient
from ..exceptions import GradientSdkError
from ..models import SingleNodeExperiment, MultiNodeExperiment
from ..serializers import SingleNodeExperimentSchema, MultiNodeExperimentSchema


class ExperimentsClient(BaseClient):
    def create_single_node(self, name, project_id, machine_type, command, ports=None, workspace=None,
                           workspace_archive=None, workspace_url=None, ignore_files=None, working_directory=None,
                           artifact_directory=None, cluster_id=None, experiment_env=None, model_type=None,
                           model_path=None, container=None, container_user=None, registry_username=None,
                           registry_password=None):
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

    def _create(self, experiment, schema_cls):
        experiment_dict = self._get_experiment_dict(experiment, schema_cls)
        response = self._get_create_response(experiment_dict)
        handle = self._process_response(response)
        return handle

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

        return experiment_dict

    def _get_workspace_url(self, experiment_dict):
        workspace_handler = S3WorkspaceHandler(experiments_api=self._client, logger_=self.logger)
        workspace_url = workspace_handler.handle(experiment_dict)
        return workspace_url

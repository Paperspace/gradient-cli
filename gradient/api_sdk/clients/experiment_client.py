from gradient import constants, config
from .base_client import BaseClient
from ..clients import http_client
from ..exceptions import GradientSdkError
from ..models import SingleNodeExperiment, MultiNodeExperiment
from ..repositories.experiments import ListExperiments, GetExperiment, ListExperimentLogs
from ..serializers import SingleNodeExperimentSchema, MultiNodeExperimentSchema
from ..utils import MessageExtractor


class ExperimentsClient(BaseClient):
    def __init__(self, *args, **kwargs):
        super(ExperimentsClient, self).__init__(*args, **kwargs)
        self.logs_client = http_client.API(config.config.CONFIG_LOG_HOST,
                                           api_key=self.api_key,
                                           logger=self.logger)

    def create_single_node(
            self,
            name,
            project_id,
            machine_type,
            command,
            ports=None,
            workspace_url=None,
            ignore_files=None,
            working_directory=None,
            artifact_directory=None,
            cluster_id=None,
            experiment_env=None,
            model_type=None,
            model_path=None,
            container=None,
            container_user=None,
            registry_username=None,
            registry_password=None,
    ):
        """Create single node experiment

        :param str name:
        :param str project_id:
        :param str machine_type:
        :param str command:
        :param str ports:
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

        experiment = SingleNodeExperiment(
            experiment_type_id=constants.ExperimentType.SINGLE_NODE,
            name=name,
            project_id=project_id,
            machine_type=machine_type,
            ports=ports,
            workspace_url=workspace_url,
            ignore_files=ignore_files,
            working_directory=working_directory,
            artifact_directory=artifact_directory,
            cluster_id=cluster_id,
            experiment_env=experiment_env,
            model_type=model_type,
            model_path=model_path,
            container=container,
            command=command,
            container_user=container_user,
            registry_username=registry_username,
            registry_password=registry_password,
        )

        handle = self._create(experiment, SingleNodeExperimentSchema)
        return handle

    def create_multi_node(
            self,
            name,
            project_id,
            experiment_type_id,
            worker_container,
            worker_machine_type,
            worker_command,
            worker_count,
            parameter_server_container,
            parameter_server_machine_type,
            parameter_server_command,
            parameter_server_count,
            ports=None,
            workspace_url=None,
            ignore_files=None,
            working_directory=None,
            artifact_directory=None,
            cluster_id=None,
            experiment_env=None,
            model_type=None,
            model_path=None,
            worker_container_user=None,
            worker_registry_username=None,
            worker_registry_password=None,
            parameter_server_container_user=None,
            parameter_server_registry_container_user=None,
            parameter_server_registry_password=None,
    ):
        """Create multi node experiment

        :param str name:
        :param str project_id:
        :param str experiment_type_id:
        :param str worker_container:
        :param str worker_machine_type:
        :param str worker_command:
        :param int worker_count:
        :param str parameter_server_container:
        :param str parameter_server_machine_type:
        :param str parameter_server_command:
        :param int parameter_server_count:
        :param str ports:
        :param str workspace_url:
        :param list[str] ignore_files:
        :param str working_directory:
        :param str artifact_directory:
        :param str cluster_id:
        :param dict experiment_env:
        :param str model_type:
        :param str model_path:
        :param str worker_container_user:
        :param str worker_registry_username:
        :param str worker_registry_password:
        :param str parameter_server_container_user:
        :param str parameter_server_registry_container_user:
        :param str parameter_server_registry_password:

        :rtype: str

        """
        experiment = MultiNodeExperiment(
            name=name,
            project_id=project_id,
            experiment_type_id=experiment_type_id,
            worker_container=worker_container,
            worker_machine_type=worker_machine_type,
            worker_command=worker_command,
            worker_count=worker_count,
            parameter_server_container=parameter_server_container,
            parameter_server_machine_type=parameter_server_machine_type,
            parameter_server_command=parameter_server_command,
            parameter_server_count=parameter_server_count,
            ports=ports,
            workspace_url=workspace_url,
            ignore_files=ignore_files,
            working_directory=working_directory,
            artifact_directory=artifact_directory,
            cluster_id=cluster_id,
            experiment_env=experiment_env,
            model_type=model_type,
            model_path=model_path,
            worker_container_user=worker_container_user,
            worker_registry_username=worker_registry_username,
            worker_registry_password=worker_registry_password,
            parameter_server_container_user=parameter_server_container_user,
            parameter_server_registry_container_user=parameter_server_registry_container_user,
            parameter_server_registry_password=parameter_server_registry_password,
        )

        handle = self._create(experiment, MultiNodeExperimentSchema)
        return handle

    def run_single_node(
            self,
            name,
            project_id,
            machine_type,
            command,
            ports=None,
            workspace_url=None,
            ignore_files=None,
            working_directory=None,
            artifact_directory=None,
            cluster_id=None,
            experiment_env=None,
            model_type=None,
            model_path=None,
            container=None,
            container_user=None,
            registry_username=None,
            registry_password=None,
    ):
        """Create and start single node experiment

        :param str name:
        :param str project_id:
        :param str machine_type:
        :param str command:
        :param str ports:
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

        experiment = SingleNodeExperiment(
            experiment_type_id=constants.ExperimentType.SINGLE_NODE,
            name=name,
            project_id=project_id,
            machine_type=machine_type,
            ports=ports,
            workspace_url=workspace_url,
            ignore_files=ignore_files,
            working_directory=working_directory,
            artifact_directory=artifact_directory,
            cluster_id=cluster_id,
            experiment_env=experiment_env,
            model_type=model_type,
            model_path=model_path,
            container=container,
            command=command,
            container_user=container_user,
            registry_username=registry_username,
            registry_password=registry_password,
        )

        handle = self._run(experiment, SingleNodeExperimentSchema)
        return handle

    def run_multi_node(
            self,
            name,
            project_id,
            experiment_type_id,
            worker_container,
            worker_machine_type,
            worker_command,
            worker_count,
            parameter_server_container,
            parameter_server_machine_type,
            parameter_server_command,
            parameter_server_count,
            ports=None,
            workspace_url=None,
            ignore_files=None,
            working_directory=None,
            artifact_directory=None,
            cluster_id=None,
            experiment_env=None,
            model_type=None,
            model_path=None,
            worker_container_user=None,
            worker_registry_username=None,
            worker_registry_password=None,
            parameter_server_container_user=None,
            parameter_server_registry_container_user=None,
            parameter_server_registry_password=None,
    ):
        """Create and start multi node experiment

        :param str name:
        :param str project_id:
        :param str experiment_type_id:
        :param str worker_container:
        :param str worker_machine_type:
        :param str worker_command:
        :param int worker_count:
        :param str parameter_server_container:
        :param str parameter_server_machine_type:
        :param str parameter_server_command:
        :param int parameter_server_count:
        :param str ports:
        :param str workspace_url:
        :param list[str] ignore_files:
        :param str working_directory:
        :param str artifact_directory:
        :param str cluster_id:
        :param dict experiment_env:
        :param str model_type:
        :param str model_path:
        :param str worker_container_user:
        :param str worker_registry_username:
        :param str worker_registry_password:
        :param str parameter_server_container_user:
        :param str parameter_server_registry_container_user:
        :param str parameter_server_registry_password:

        :rtype: str

        """
        experiment = MultiNodeExperiment(
            name=name,
            project_id=project_id,
            experiment_type_id=experiment_type_id,
            worker_container=worker_container,
            worker_machine_type=worker_machine_type,
            worker_command=worker_command,
            worker_count=worker_count,
            parameter_server_container=parameter_server_container,
            parameter_server_machine_type=parameter_server_machine_type,
            parameter_server_command=parameter_server_command,
            parameter_server_count=parameter_server_count,
            ports=ports,
            workspace_url=workspace_url,
            ignore_files=ignore_files,
            working_directory=working_directory,
            artifact_directory=artifact_directory,
            cluster_id=cluster_id,
            experiment_env=experiment_env,
            model_type=model_type,
            model_path=model_path,
            worker_container_user=worker_container_user,
            worker_registry_username=worker_registry_username,
            worker_registry_password=worker_registry_password,
            parameter_server_container_user=parameter_server_container_user,
            parameter_server_registry_container_user=parameter_server_registry_container_user,
            parameter_server_registry_password=parameter_server_registry_password,
        )

        handle = self._run(experiment, MultiNodeExperimentSchema)
        return handle

    def start(self, experiment_id):
        """Start existing experiment

        :param str experiment_id:
        :rtype: http_client.GradientResponse
        """
        response = self._get_start_response(experiment_id)
        gradient_response = self._interpret_response(response)
        return gradient_response

    def stop(self, experiment_id):
        """Stop running experiment

        :param str experiment_id:
        :rtype: http_client.GradientResponse
        """
        response = self._get_stop_response(experiment_id)
        gradient_response = self._interpret_response(response)
        return gradient_response

    def list(self, project_id=None):
        """Get a list of experiments. Optionally filter by project ID

        :param str|list|None project_id:
        :rtype: list[SingleNodeExperiment|MultiNodeExperiment]
        """
        experiments = ListExperiments(self.client).list(project_id=project_id)
        return experiments

    def get(self, experiment_id):
        """Get experiment instance

        :param str experiment_id:
        :rtype: SingleNodeExperiment|MultiNodeExperiment
        """
        experiment = GetExperiment(self.client).get(experiment_id=experiment_id)
        return experiment

    def logs(self, experiment_id, line=0, limit=10000):
        """Get list of logs for an experiment

        :param str experiment_id:
        :param int line:
        :param int limit:
        """
        logs = ListExperimentLogs(self.logs_client).list(experiment_id, line, limit)
        return logs

    def yield_logs(self, experiment_id, line=0, limit=10000):
        """Get log generator. Polls the API for new logs

        :param str experiment_id:
        :param int line:
        :param int limit:
        """
        logs_generator = ListExperimentLogs(self.logs_client).yield_logs(experiment_id, line, limit)
        return logs_generator

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
        response = self.client.post("/experiments/", json=experiment_dict)
        return response

    def _get_run_response(self, experiment_dict):
        response = self.client.post("/experiments/create_and_start/", json=experiment_dict)
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

        ignore_files = experiment_dict.pop("ignore_files", None)
        if ignore_files:
            experiment_dict["ignore_files"] = self._list_to_comma_separated(ignore_files)

        return experiment_dict

    @staticmethod
    def _interpret_response(response):
        gradient_response = http_client.GradientResponse.interpret_response(response)
        return gradient_response

    def _get_start_response(self, experiment_id):
        url = "/experiments/{}/start/".format(experiment_id)
        response = self.client.put(url)
        return response

    def _get_stop_response(self, experiment_id):
        url = "/experiments/{}/stop/".format(experiment_id)
        response = self.client.put(url)
        return response

from gradient import constants, config
from . import http_client
from .base_client import BaseClient
from .. import repositories, models, serializers


class ExperimentsClient(BaseClient):
    HOST_URL = config.config.CONFIG_EXPERIMENTS_HOST
    LOG_HOST_URL = config.config.CONFIG_LOG_HOST

    def __init__(self, api_key, *args, **kwargs):
        super(ExperimentsClient, self).__init__(api_key, *args, **kwargs)
        self.logs_client = http_client.API(api_url=self.LOG_HOST_URL,
                                           api_key=api_key,
                                           logger=self.logger)

    def create_single_node(
            self,
            name,
            project_id,
            machine_type,
            command,
            ports=None,
            workspace_url=None,
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

        :returns: experiment handle
        :rtype: str
        """

        experiment = models.SingleNodeExperiment(
            experiment_type_id=constants.ExperimentType.SINGLE_NODE,
            name=name,
            project_id=project_id,
            machine_type=machine_type,
            ports=ports,
            workspace_url=workspace_url,
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

        handle = self._create(experiment, serializers.SingleNodeExperimentSchema)
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

        :returns: experiment handle
        :rtype: str
        """
        experiment = models.MultiNodeExperiment(
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

        handle = self._create(experiment, serializers.MultiNodeExperimentSchema)
        return handle

    def run_single_node(
            self,
            name,
            project_id,
            machine_type,
            command,
            ports=None,
            workspace_url=None,
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

        :returns: experiment handle
        :rtype: str
        """

        experiment = models.SingleNodeExperiment(
            experiment_type_id=constants.ExperimentType.SINGLE_NODE,
            name=name,
            project_id=project_id,
            machine_type=machine_type,
            ports=ports,
            workspace_url=workspace_url,
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

        handle = self._run(experiment, serializers.SingleNodeExperimentSchema)
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

        :returns: experiment handle
        :rtype: str

        """
        experiment = models.MultiNodeExperiment(
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

        handle = self._run(experiment, serializers.MultiNodeExperimentSchema)
        return handle

    def start(self, experiment_id):
        """Start existing experiment

        :param str experiment_id:
        """
        repositories.StartExperiment(self.client).start(experiment_id)

    def stop(self, experiment_id):
        """Stop running experiment

        :param str experiment_id:
        """
        repositories.StopExperiment(self.client).stop(experiment_id)

    def list(self, project_id=None):
        """Get a list of experiments. Optionally filter by project ID

        :param str|list|None project_id:
        :rtype: list[SingleNodeExperiment|MultiNodeExperiment]
        """
        experiments = repositories.ListExperiments(self.client).list(project_id=project_id)
        return experiments

    def get(self, experiment_id):
        """Get experiment instance

        :param str experiment_id:
        :rtype: SingleNodeExperiment|MultiNodeExperiment
        """
        experiment = repositories.GetExperiment(self.client).get(experiment_id=experiment_id)
        return experiment

    def logs(self, experiment_id, line=0, limit=10000):
        """Get list of logs for an experiment

        :param str experiment_id:
        :param int line:
        :param int limit:

        :returns: list of LogRows
        :rtype: list[models.LogRow]
        """
        logs = repositories.ListExperimentLogs(self.logs_client).list(experiment_id, line, limit)
        return logs

    def yield_logs(self, experiment_id, line=0, limit=10000):
        """Get log generator. Polls the API for new logs

        :param str experiment_id:
        :param int line:
        :param int limit:

        :returns: generator yielding LogRow instances
        :rtype: Iterator[models.LogRow]
        """
        logs_generator = repositories.ListExperimentLogs(client=self.logs_client).yield_logs(experiment_id, line, limit)
        return logs_generator

    def _create(self, experiment, schema_cls):
        handle = repositories.CreateExperiment(client=self.client).create(experiment, schema_cls)
        return handle

    def _run(self, experiment, schema_cls):
        handle = repositories.RunExperiment(client=self.client).create(experiment, schema_cls)
        return handle

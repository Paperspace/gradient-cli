from . import base_client
from .. import models, repositories


class HyperparameterJobsClient(base_client.BaseClient):
    def create(
            self,
            name,
            project_id,
            tuning_command,
            worker_container,
            worker_machine_type,
            worker_command,
            worker_count,
            is_preemptible=True,
            ports=None,
            workspace_url=None,
            artifact_directory=None,
            cluster_id=None,
            experiment_env=None,
            trigger_event_id=None,
            model_type=None,
            model_path=None,
            dockerfile_path=None,
            registry_username=None,
            registry_password=None,
            container_user=None,
            working_directory=None,
            use_dockerfile=False,
    ):
        """Create hyperparameter tuning job

        :param str name:
        :param str project_id:
        :param str tuning_command:
        :param str worker_container:
        :param str worker_machine_type:
        :param str worker_command:
        :param str worker_count:
        :param bool is_preemptible:
        :param list[str] ports:
        :param str workspace_url:
        :param str artifact_directory:
        :param str cluster_id:
        :param dict experiment_env:
        :param str trigger_event_id:
        :param str model_type:
        :param str model_path:
        :param str dockerfile_path:
        :param str registry_username:
        :param str registry_password:
        :param str container_user:
        :param str working_directory:
        :param bool use_dockerfile:

        :rtype str
        """

        hyperparameter = models.Hyperparameter(
            name=name,
            project_id=project_id,
            tuning_command=tuning_command,
            worker_container=worker_container,
            worker_machine_type=worker_machine_type,
            worker_command=worker_command,
            worker_count=worker_count,
            is_preemptible=is_preemptible,
            ports=ports,
            workspace_url=workspace_url,
            artifact_directory=artifact_directory,
            cluster_id=cluster_id,
            experiment_env=experiment_env,
            trigger_event_id=trigger_event_id,
            model_type=model_type,
            model_path=model_path,
            dockerfile_path=dockerfile_path,
            registry_username=registry_username,
            registry_password=registry_password,
            container_user=container_user,
            working_directory=working_directory,
            use_dockerfile=use_dockerfile,
        )

        handle = repositories.CreateHyperparameterJob(client=self.client).create(hyperparameter)
        return handle

    def run(
            self,
            name,
            project_id,
            tuning_command,
            worker_container,
            worker_machine_type,
            worker_command,
            worker_count,
            is_preemptible=True,
            ports=None,
            workspace_url=None,
            artifact_directory=None,
            cluster_id=None,
            experiment_env=None,
            trigger_event_id=None,
            model_type=None,
            model_path=None,
            dockerfile_path=None,
            registry_username=None,
            registry_password=None,
            container_user=None,
            working_directory=None,
            use_dockerfile=False,
    ):
        """Create and start hyperparameter tuning job

        :param str name:
        :param str project_id:
        :param str tuning_command:
        :param str worker_container:
        :param str worker_machine_type:
        :param str worker_command:
        :param str worker_count:
        :param bool is_preemptible:
        :param list[str] ports:
        :param str workspace_url:
        :param str artifact_directory:
        :param str cluster_id:
        :param dict experiment_env:
        :param str trigger_event_id:
        :param str model_type:
        :param str model_path:
        :param str dockerfile_path:
        :param str registry_username:
        :param str registry_password:
        :param str container_user:
        :param str working_directory:
        :param bool use_dockerfile:

        :rtype str
        """

        hyperparameter = models.Hyperparameter(
            name=name,
            project_id=project_id,
            tuning_command=tuning_command,
            worker_container=worker_container,
            worker_machine_type=worker_machine_type,
            worker_command=worker_command,
            worker_count=worker_count,
            is_preemptible=is_preemptible,
            ports=ports,
            workspace_url=workspace_url,
            artifact_directory=artifact_directory,
            cluster_id=cluster_id,
            experiment_env=experiment_env,
            trigger_event_id=trigger_event_id,
            model_type=model_type,
            model_path=model_path,
            dockerfile_path=dockerfile_path,
            registry_username=registry_username,
            registry_password=registry_password,
            container_user=container_user,
            working_directory=working_directory,
            use_dockerfile=use_dockerfile,
        )

        handle = repositories.CreateAndStartHyperparameterJob(client=self.client).create(hyperparameter)
        return handle

    def get(self, id_):
        """Get Hyperparameter tuning job's instance

        :param str id_:

        :rtype: models.Hyperparameter
        """
        job = repositories.GetHyperparameterTuningJob(self.client).get(id=id_)
        return job

    def start(self, id_):
        """Start existing hyperparameter tuning job

        :param str id_:
        """
        repositories.StartHyperparameterTuningJob(self.client).start(id_=id_)

    def list(self):
        """Get a list of hyperparameter tuning jobs

        :rtype: list[models.Hyperparameter]
        """
        experiments = repositories.ListHyperparameterJobs(self.client).list()
        return experiments

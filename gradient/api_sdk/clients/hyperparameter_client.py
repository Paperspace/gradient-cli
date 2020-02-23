from . import base_client
from .. import models, repositories


class HyperparameterJobsClient(base_client.BaseClient):
    entity = "experiment"

    def create(
            self,
            name,
            project_id,
            tuning_command,
            worker_container,
            worker_machine_type,
            worker_command,
            worker_count,
            worker_container_user=None,
            worker_registry_username=None,
            worker_registry_password=None,
            is_preemptible=False,
            ports=None,
            workspace_url=None,
            artifact_directory=None,
            cluster_id=None,
            experiment_env=None,
            trigger_event_id=None,
            model_type=None,
            model_path=None,
            dockerfile_path=None,
            hyperparameter_server_registry_username=None,
            hyperparameter_server_registry_password=None,
            hyperparameter_server_container=None,
            hyperparameter_server_container_user=None,
            hyperparameter_server_machine_type=None,
            working_directory=None,
            use_dockerfile=False,
            tags=None,
    ):
        """Create hyperparameter tuning job
        :param str name: Name of new experiment [required]
        :param str project_id: Project ID [required]
        :param str tuning_command: Tuning command [required]
        :param str worker_container: Worker container  [required]
        :param str worker_machine_type: Worker machine type  [required]
        :param str worker_command: Worker command  [required]
        :param int worker_count: Worker count  [required]
        :param str worker_container_user: Worker Container user
        :param str worker_registry_username: Worker registry username
        :param str worker_registry_password: Worker registry password
        :param bool is_preemptible: Flag: is preemptible
        :param str ports: Port to use in new experiment
        :param str workspace_url: Project git repository url
        :param str artifact_directory: Artifacts directory
        :param str cluster_id: Cluster ID
        :param dict experiment_env: Environment variables (in JSON)
        :param str trigger_event_id: GradientCI trigger event id
        :param str model_type: Model type
        :param str model_path: Model path
        :param str dockerfile_path: Path to dockerfile in project
        :param str hyperparameter_server_registry_username: Hyperparameter server registry username
        :param str hyperparameter_server_registry_password: Hyperparameter server registry password
        :param str hyperparameter_server_container: Hyperparameter server container
        :param str hyperparameter_server_container_user: Hyperparameter server container user
        :param str hyperparameter_server_machine_type: Hyperparameter server machine type
        :param str working_directory: Working directory for the experiment
        :param bool use_dockerfile: Flag: use dockerfile
        :param list[str] tags: List of tags

        :returns: ID of a new job
        :rtype: str
        """

        if not is_preemptible:
            is_preemptible = None

        if use_dockerfile is False:
            use_dockerfile = None

        hyperparameter = models.Hyperparameter(
            name=name,
            project_id=project_id,
            tuning_command=tuning_command,
            worker_container=worker_container,
            worker_container_user=worker_container_user,
            worker_machine_type=worker_machine_type,
            worker_command=worker_command,
            worker_count=worker_count,
            worker_registry_username=worker_registry_username,
            worker_registry_password=worker_registry_password,
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
            hyperparameter_server_machine_type=hyperparameter_server_machine_type,
            hyperparameter_server_registry_username=hyperparameter_server_registry_username,
            hyperparameter_server_registry_password=hyperparameter_server_registry_password,
            hyperparameter_server_container=hyperparameter_server_container,
            hyperparameter_server_container_user=hyperparameter_server_container_user,
            working_directory=working_directory,
            use_dockerfile=use_dockerfile,
        )

        repository = self.build_repository(repositories.CreateHyperparameterJob)
        handle = repository.create(hyperparameter)

        if tags:
            self.add_tags(entity_id=handle, entity=self.entity, tags=tags)

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
            worker_registry_username=None,
            worker_registry_password=None,
            worker_container_user=None,
            is_preemptible=False,
            ports=None,
            workspace_url=None,
            artifact_directory=None,
            cluster_id=None,
            experiment_env=None,
            trigger_event_id=None,
            model_type=None,
            model_path=None,
            dockerfile_path=None,
            hyperparameter_server_registry_username=None,
            hyperparameter_server_registry_password=None,
            hyperparameter_server_container_user=None,
            hyperparameter_server_container=None,
            hyperparameter_server_machine_type=None,
            working_directory=None,
            use_dockerfile=False,
            tags=None,
    ):
        """Create and start hyperparameter tuning job

        :param str name: Name of new experiment  [required]
        :param str project_id: Project ID  [required]
        :param str tuning_command: Tuning command  [required]
        :param str worker_container: Worker container  [required]
        :param str worker_machine_type: Worker machine type  [required]
        :param str worker_command: Worker command  [required]
        :param int worker_count: Worker count  [required]
        :param str worker_container_user: Worker container user
        :param worker_registry_password: Worker registry password
        :param worker_registry_username: Worker registry username
        :param bool is_preemptible: Flag: is preemptible
        :param str ports: Port to use in new experiment
        :param str workspace_url: Project git repository url
        :param str artifact_directory: Artifacts directory
        :param str cluster_id: Cluster ID
        :param dict experiment_env: Environment variables (in JSON)
        :param str trigger_event_id: GradientCI trigger event id
        :param str model_type: Model type
        :param str model_path: Model path
        :param str dockerfile_path: Path to dockerfile
        :param str hyperparameter_server_registry_username: container registry username
        :param str hyperparameter_server_registry_password: container registry password
        :param str hyperparameter_server_container_user: hps container user
        :param str hyperparameter_server_container: hps container
        :param str hyperparameter_server_machine_type: hps machine type
        :param str working_directory: Working directory for the experiment
        :param bool use_dockerfile: Flag: use dockerfile
        :param list[str] tags: List of tags

        :returns: ID of a new job
        :rtype: str
        """

        if not is_preemptible:
            is_preemptible = None

        if use_dockerfile is False:
            use_dockerfile = None

        hyperparameter = models.Hyperparameter(
            name=name,
            project_id=project_id,
            tuning_command=tuning_command,
            worker_container=worker_container,
            worker_machine_type=worker_machine_type,
            worker_command=worker_command,
            worker_count=worker_count,
            worker_container_user=worker_container_user,
            worker_registry_username=worker_registry_username,
            worker_registry_password=worker_registry_password,
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
            hyperparameter_server_registry_username=hyperparameter_server_registry_username,
            hyperparameter_server_registry_password=hyperparameter_server_registry_password,
            hyperparameter_server_container_user=hyperparameter_server_container_user,
            hyperparameter_server_container=hyperparameter_server_container,
            hyperparameter_server_machine_type=hyperparameter_server_machine_type,
            working_directory=working_directory,
            use_dockerfile=use_dockerfile,
        )

        repository = self.build_repository(repositories.CreateAndStartHyperparameterJob)
        handle = repository.create(hyperparameter)

        if tags:
            self.add_tags(entity_id=handle, entity=self.entity, tags=tags)

        return handle

    def get(self, id):
        """Get Hyperparameter tuning job's instance

        :param str id: Hyperparameter job id

        :returns: instance of Hyperparameter
        :rtype: models.Hyperparameter
        """

        repository = self.build_repository(repositories.GetHyperparameterTuningJob)
        job = repository.get(id=id)
        return job

    def start(self, id):
        """Start existing hyperparameter tuning job

        :param str id: Hyperparameter job id
        :raises: exceptions.GradientSdkError
        """

        repository = self.build_repository(repositories.StartHyperparameterTuningJob)
        repository.start(id_=id)

    def list(self):
        """Get a list of hyperparameter tuning jobs

        :rtype: list[models.Hyperparameter]
        """
        repository = self.build_repository(repositories.ListHyperparameterJobs)
        experiments = repository.list()
        return experiments

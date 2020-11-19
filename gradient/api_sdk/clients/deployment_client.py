"""
Deployment related client handler logic.

Remember that in code snippets all highlighted lines are required other lines are optional.
"""
from .base_client import BaseClient, TagsSupportMixin
from .. import config, models, repositories


class DeploymentsClient(TagsSupportMixin, BaseClient):
    """
    Client to handle deployment related actions.

    How to create instance of deployment client:

    .. code-block:: python
        :linenos:
        :emphasize-lines: 4

        from gradient import DeploymentsClient

        deployment_client = DeploymentsClient(
            api_key='your_api_key_here'
        )
    """
    HOST_URL = config.config.CONFIG_HOST
    entity = "deployment"

    def create(
            self,
            deployment_type,
            name,
            machine_type,
            image_url,
            instance_count=None,
            model_id=None,
            container_model_path=None,
            image_username=None,
            image_password=None,
            image_server=None,
            container_url_path=None,
            endpoint_url_path=None,
            method=None,
            docker_args=None,
            env=None,
            api_type=None,
            ports=None,
            cluster_id=None,
            auth_username=None,
            auth_password=None,
            tags=None,
            command=None,
            workspace_url=None,
            workspace_ref=None,
            workspace_username=None,
            workspace_password=None,
            project_id=None,
            autoscaling=None,
    ):
        """
        Method to create a Deployment instance.

        To create a new Deployment, you must first create a Model. With a Model available, use the ``create`` subcommand
        and specify all of the following parameters: deployment type, base image, name, machine type, and container
        image for serving, as well as the instance count:

        .. code-block:: python
            :linenos:
            :emphasize-lines: 4

            from gradient import DeploymentsClient

            deployment_client = DeploymentsClient(
                api_key='your_api_key_here'
            )


        To obtain your Model ID, you can run ``command gradient models list`` and copy the target Model ID from
        your available Models.

        :param str deployment_type: Model deployment type. Only TensorFlow Model deployment type is currently supported  [required]
        :param str model_id: ID of a trained model [required]
        :param str name: Human-friendly name for new model deployment [required]
        :param str machine_type: [G1|G6|G12|K80|P100|GV100] Type of machine for new deployment [required]
        :param str image_url: Docker image for model deployment  [required]
        :param int instance_count: Number of machine instances  [required]
        :param str container_model_path: Container model path
        :param str image_username: Username used to access docker image
        :param str image_password: Password used to access docker image
        :param str image_server: Docker image server
        :param str container_url_path: Container URL path
        :param str endpoint_url_path: Endpoint URL path
        :param str method: Method
        :param list[str]|tuple[str] docker_args: List of docker args
        :param dict[str,str] env: Environmental variables
        :param str api_type: Type of API (REST/GRPC)
        :param str ports: Ports
        :param str cluster_id: cluster ID
        :param str auth_username: Username
        :param str auth_password: Password
        :param list[str] tags: List of tags
        :param str command: Deployment command
        :param str workspace_url: Project git or s3repository url
        :param str workspace_ref: Git commit hash, branch name or tag
        :param str workspace_username: Project git repository username
        :param str workspace_password: Project git repository password
        :param str project_id: Project ID
        :param models.AutoscalingDefinition autoscaling: Deployment autoscaling definition

        :returns: Created deployment id
        :rtype: str
        """
        deployment = models.Deployment(
            deployment_type=deployment_type,
            model_id=model_id,
            name=name,
            machine_type=machine_type,
            image_url=image_url,
            instance_count=instance_count,
            container_model_path=container_model_path,
            image_username=image_username,
            image_password=image_password,
            image_server=image_server,
            container_url_path=container_url_path,
            endpoint_url_path=endpoint_url_path,
            method=method,
            docker_args=docker_args,
            env=env,
            api_type=api_type,
            ports=ports,
            cluster_id=cluster_id,
            auth_username=auth_username,
            auth_password=auth_password,
            command=command,
            workspace_url=workspace_url,
            workspace_ref=workspace_ref,
            workspace_username=workspace_username,
            workspace_password=workspace_password,
            project_id=project_id,
            autoscaling=autoscaling,
        )

        repository = self.build_repository(repositories.CreateDeployment)
        deployment_id = repository.create(deployment)
        if tags:
            self.add_tags(entity_id=deployment_id, tags=tags)
        return deployment_id

    def get(self, deployment_id):
        """Get deployment instance

        :param str deployment_id: Deployment ID

        :return: Deployment instance
        :rtype: models.Deployment
        """
        repository = self.build_repository(repositories.GetDeployment)
        deployment = repository.get(deployment_id=deployment_id)
        return deployment

    def start(self, deployment_id):
        """
        Start deployment

        *EXAMPLE*::

            gradient deployments start --id <your-deployment-id>

        :param str deployment_id: Deployment ID
        """

        repository = self.build_repository(repositories.StartDeployment)
        repository.start(deployment_id)

    def stop(self, deployment_id):
        """
        Stop deployment

        *EXAMPLE*::

            gradient deployments stop --id <your-deployment-id>

        :param deployment_id: Deployment ID
        """

        repository = self.build_repository(repositories.StopDeployment)
        repository.stop(deployment_id)

    def list(self, state=None, project_id=None, model_id=None, tags=None):
        """
        List deployments with optional filtering

        :param str state: state to filter deployments
        :param str project_id: project ID to filter deployments
        :param str model_id: model ID to filter deployments
        :param list[str]|tuple[str] tags: tags to filter deployments with OR

        :returns: List of Deployment model instances
        :rtype: list[models.Deployment]
        """

        repository = self.build_repository(repositories.ListDeployments)
        deployments = repository.list(state=state, project_id=project_id, model_id=model_id, tags=tags)
        return deployments

    def delete(self, deployment_id):
        repository = self.build_repository(repositories.DeleteDeployment)
        repository.delete(deployment_id)

    def update(
            self,
            deployment_id,
            deployment_type=None,
            model_id=None,
            name=None,
            machine_type=None,
            image_url=None,
            instance_count=None,
            container_model_path=None,
            image_username=None,
            image_password=None,
            image_server=None,
            container_url_path=None,
            endpoint_url_path=None,
            method=None,
            docker_args=None,
            env=None,
            api_type=None,
            ports=None,
            cluster_id=None,
            auth_username=None,
            auth_password=None,
            workspace_url=None,
            workspace_ref=None,
            workspace_username=None,
            workspace_password=None,
            project_id=None,
            command=None,
            autoscaling=None,
    ):
        deployment = models.Deployment(
            deployment_type=deployment_type,
            model_id=model_id,
            name=name,
            machine_type=machine_type,
            image_url=image_url,
            instance_count=instance_count,
            container_model_path=container_model_path,
            image_username=image_username,
            image_password=image_password,
            image_server=image_server,
            container_url_path=container_url_path,
            endpoint_url_path=endpoint_url_path,
            method=method,
            docker_args=docker_args,
            env=env,
            api_type=api_type,
            ports=ports,
            cluster_id=cluster_id,
            auth_username=auth_username,
            auth_password=auth_password,
            workspace_url=workspace_url,
            workspace_ref=workspace_ref,
            workspace_username=workspace_username,
            workspace_password=workspace_password,
            project_id=project_id,
            command=command,
            autoscaling=autoscaling,
        )

        repository = self.build_repository(repositories.UpdateDeployment)
        repository.update(deployment_id, deployment)

    def get_metrics(self, deployment_id, start=None, end=None, interval="30s", built_in_metrics=None):
        """Get model deployment metrics

        :param str deployment_id: ID of deployment
        :param datetime.datetime|str start:
        :param datetime.datetime|str end:
        :param str interval:
        :param list[str] built_in_metrics: List of metrics to get if different than default
                    Available builtin metrics: cpuPercentage, memoryUsage, gpuMemoryFree, gpuMemoryUsed, gpuPowerDraw,
                                            gpuTemp, gpuUtilization, gpuMemoryUtilization

        :returns: Metrics of a model deployment job
        :rtype: dict[str,dict[str,list[dict]]]
        """

        repository = self.build_repository(repositories.GetDeploymentMetrics)
        metrics = repository.get(
            id=deployment_id,
            start=start,
            end=end,
            interval=interval,
            built_in_metrics=built_in_metrics,
        )
        return metrics

    
    def list_metrics(self, deployment_id, start=None, end=None, interval="30s"):
        """List model deployment metrics

        :param str deployment_id: ID of deployment
        :param datetime.datetime|str start:
        :param datetime.datetime|str end:
        :param str interval:
        :returns: Metrics of a model deployment job
        :rtype: dict[str,dict[str,list[dict]]]
        """

        repository = self.build_repository(repositories.ListDeploymentMetrics)
        metrics = repository.get(
            id=deployment_id,
            start=start,
            end=end,
            interval=interval,
        )
        return metrics

    def stream_metrics(self, deployment_id, interval="30s", built_in_metrics=None):
        """Stream live model deployment metrics

        :param str deployment_id: ID of model deployment
        :param str interval:
        :param list[str] built_in_metrics: List of metrics to get if different than default
                    Available builtin metrics: cpuPercentage, memoryUsage, gpuMemoryFree, gpuMemoryUsed, gpuPowerDraw,
                                            gpuTemp, gpuUtilization, gpuMemoryUtilization

        :returns: Generator object yielding live model deployment metrics
        :rtype: Iterable[dict]
        """

        repository = self.build_repository(repositories.StreamDeploymentMetrics)
        metrics = repository.stream(
            id=deployment_id,
            interval=interval,
            built_in_metrics=built_in_metrics,
        )
        return metrics

    def logs(self, deployment_id, line=1, limit=10000):
        """Show list of latest logs from the specified deployment.

        :param str deployment_id: Deployment Id
        :param int line: line number at which logs starts to display on screen
        :param int limit: maximum lines displayed on screen, default set to 10 000

        :returns: list of LogRows
        :rtype: list[models.LogRow]
        """

        repository = self.build_repository(repositories.ListDeploymentLogs)
        logs = repository.list(id=deployment_id, line=line, limit=limit)
        return logs

    def yield_logs(self, deployment_id, line=1, limit=10000):
        """Get log generator. Polls the API for new logs

        :param str deployment_id: Deployment Id
        :param int line: line number at which logs starts to display on screen
        :param int limit: maximum lines displayed on screen, default set to 10 000

        :returns: generator yielding LogRow instances
        :rtype: Iterator[models.LogRow]
        """

        repository = self.build_repository(repositories.ListDeploymentLogs)
        logs = repository.yield_logs(id=deployment_id, line=line, limit=limit)
        return logs

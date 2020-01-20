"""
Deployment related client handler logic.

Remember that in code snippets all highlighted lines are required other lines are optional.
"""
from .base_client import BaseClient
from .. import config, models, repositories


class DeploymentsClient(BaseClient):
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

    def create(
            self,
            deployment_type,
            model_id, name,
            machine_type,
            image_url,
            instance_count,
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
            use_vpc=False,
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
        :param bool use_vpc:

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
        )

        repository = repositories.CreateDeployment(api_key=self.api_key, logger=self.logger)
        deployment_id = repository.create(deployment, use_vpc=use_vpc)
        return deployment_id

    def get(self, deployment_id):
        """Get deployment instance

        :param str deployment_id: Deployment ID

        :return: Deployment instance
        :rtype: models.Deployment
        """
        repository = repositories.GetDeployment(self.api_key, logger=self.logger)
        deployment = repository.get(deployment_id=deployment_id)
        return deployment

    def start(self, deployment_id, use_vpc=False):
        """
        Start deployment

        *EXAMPLE*::

            gradient deployments start --id <your-deployment-id>

        :param str deployment_id: Deployment ID
        :param bool use_vpc:
        """

        repository = repositories.StartDeployment(api_key=self.api_key, logger=self.logger)
        repository.start(deployment_id, use_vpc=use_vpc)

    def stop(self, deployment_id, use_vpc=False):
        """
        Stop deployment

        *EXAMPLE*::

            gradient deployments stop --id <your-deployment-id>

        :param deployment_id: Deployment ID
        :param bool use_vpc:
        """

        repository = repositories.StopDeployment(api_key=self.api_key, logger=self.logger)
        repository.stop(deployment_id, use_vpc=use_vpc)

    def list(self, state=None, project_id=None, model_id=None, use_vpc=False):
        """
        List deployments with optional filtering

        :param str state:
        :param str project_id:
        :param str model_id:
        :param bool use_vpc:
        """

        repository = repositories.ListDeployments(api_key=self.api_key, logger=self.logger)
        deployments = repository.list(state=state, project_id=project_id, model_id=model_id, use_vpc=use_vpc)
        return deployments

    def delete(self, deployment_id, use_vpc=False):
        repository = repositories.DeleteDeployment(api_key=self.api_key, logger=self.logger)
        repository.delete(deployment_id, use_vpc=use_vpc)

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
            use_vpc=False,
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
        )

        repository = repositories.UpdateDeployment(api_key=self.api_key, logger=self.logger)
        repository.update(deployment_id, deployment, use_vpc=use_vpc)

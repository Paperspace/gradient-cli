"""
Deployment related client handler logic.

Remember that in code snippets all highlighted lines are required other lines are optional.
"""
from gradient import config
from .base_client import BaseClient
from .. import models, repositories


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
            cluster_id=None,
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

        :param  str deployment_type: Model deployment type. Only TensorFlow Model deployment type is currently supported  [required]
        :param str model_id: ID of a trained model [required]
        :param str name: Human-friendly name for new model deployment [required]
        :param str machine_type: [G1|G6|G12|K80|P100|GV100] Type of machine for new deployment [required]
        :param str image_url: Docker image for model deployment  [required]
        :param int instance_count: Number of machine instances  [required]
        :param str cluster_id: cluster ID
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
            cluster_id=cluster_id,
        )

        repository = repositories.CreateDeployment(api_key=self.api_key, logger=self.logger)
        deployment_id = repository.create(deployment, use_vpc=use_vpc)
        return deployment_id

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

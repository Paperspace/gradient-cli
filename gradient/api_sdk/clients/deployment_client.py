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

    def create(self, deployment_type, model_id, name, machine_type, image_url, instance_count):
        """
        Method to create a Deployment instance.

        To create a new Deployment, you must first create a Model. With a Model available, use the ``create`` subcommand
        and specify all of the following parameters: deployment type, base image, name, machine type, and container
        image for serving, as well as the instance count:

        .. code-block:: python
            :linenos:
            :emphasize-lines: 4,5,6,,7,8,9

            from gradient import DeploymentsClient

            deployment_handle = deployment_client.create(
                deployment_type='TFServing',
                model_id='your_model_id_here,
                name='Some model name here',
                machine_type='K80',
                image_url='tensorflow/serving:latest-gpu',
                instance_count=2
            )

        To obtain your Model ID, you can run ``command gradient models list`` and copy the target Model ID from
        your available Models.

        :param str deployment_type: Model deployment type. Only TensorFlow Model deployment type is currently supported  [required]
        :param str model_id: ID of a trained model [required]
        :param str name: Human-friendly name for new model deployment [required]
        :param str machine_type: Type of machine for new deployment [required]

            We recommend to choose one of this:

            .. code-block::

                K80
                P100
                TPU
                GV100
                GV100x8
                G1
                G6
                G12

        :param str image_url: Docker image for model deployment  [required]
        :param int instance_count: Number of machine instances  [required]

        :returns: Created deployment id
        :rtype: str
        """
        deployment = models.Deployment(
            deployment_type=deployment_type,
            model_id=model_id,
            name=name,
            machine_type=machine_type,
            image_url=image_url,
            instance_count=instance_count
        )

        id_ = repositories.CreateDeployment(self.client).create(deployment)
        return id_

    def start(self, deployment_id):
        """
        Method to start deployment.

        .. code-block:: python
            :linenos:
            :emphasize-lines: 4

            from gradient import DeploymentsClient

            deployment_handle = deployment_client.start(
                deployment_id='deployment_id_here',
            )

        :param str deployment_id: Deployment ID
        :raises: exceptions.GradientSdkError
        """
        repositories.StartStopDeployment(self.client).start(deployment_id)

    def stop(self, deployment_id):
        """
        Method to stop deployment

        .. code-block:: python
            :linenos:
            :emphasize-lines: 4

            from gradient import DeploymentsClient

            deployment_handle = deployment_client.stop(
                deployment_id='deployment_id_here',
            )

        :param deployment_id: Deployment ID
        :raises: exceptions.GradientSdkError
        """
        repositories.StartStopDeployment(self.client).start(deployment_id, is_running=False)

    def list(self, state=None, project_id=None, model_id=None):
        """
        List deployments with optional filtering

        To view all running deployments in your team, run::

        .. code-block:: python
            :linenos:

            from gradient import DeploymentsClient

            deployment_handle = deployment_client.list(
                state='RUNNING',
            )

        :param None|str state: to limit results by state of deployment

            Available states:

            .. code-block::

                    BUILDING
                    PROVISIONING
                    STARTING
                    RUNNING
                    STOPPING
                    STOPPED
                    ERROR

        :param None|str project_id: Use to filter by project ID
        :param None|str model_id: Use to filter by model ID

        :returns: List of deployments
        :rtype: list
        """
        return repositories.ListDeployments(self.client).list(state=state, project_id=project_id, model_id=model_id)

from gradient import config
from gradient.api_sdk.utils import MessageExtractor
from .base_client import BaseClient
from .. import models, repositories, serializers
from ..exceptions import GradientSdkError


class DeploymentsClient(BaseClient):
    HOST_URL = config.config.CONFIG_HOST

    def create(self, deployment_type, model_id, name, machine_type, image_url, instance_count):
        """
        Method to create a Deployment instance.

        To create a new Deployment, you must first create a Model. With a Model available, use the ``create`` subcommand
        and specify all of the following parameters: deployment type, base image, name, machine type, and container
        image for serving, as well as the instance count:

        *EXAMPLE*::

            gradient deployments create
            --deploymentType TFServing
            --modelId <your-model-id>
            --name "Sample Model"
            --machineType K80
            --imageUrl tensorflow/serving:latest-gpu
            --instanceCount 2


        To obtain your Model ID, you can run ``command gradient models list`` and copy the target Model ID from
        your available Models.

        :param deployment_type: Model deployment type. Only TensorFlow Model deployment type is currently supported  [required]
        :param modelId: ID of a trained model [required]
        :param name: Human-friendly name for new model deployment [required]
        :param machine_type: [G1|G6|G12|K80|P100|GV100] Type of machine for new deployment [required]
        :param image_url: Docker image for model deployment  [required]
        :param instance_count: Number of machine instances  [required]
        :return: Created deployment id
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
        Start deployment

        *EXAMPLE*::

            gradient deployments start --id <your-deployment-id>

        :param str deployment_id: Deployment ID
        """
        return self._get_post_response(deployment_id)

    def stop(self, deployment_id):
        """
        Stop deployment

        *EXAMPLE*::

            gradient deployments stop --id <your-deployment-id>

        :param deployment_id: Deployment ID
        """
        return self._get_post_response(deployment_id, is_running=False)

    def list(self, filters):
        """
        List deployments with optional filtering

        To view all running deployments in your team, run::

            gradient deployments list --state RUNNING

        Options::

          --state [BUILDING|PROVISIONING|STARTING|RUNNING|STOPPING|STOPPED|ERROR] Filter by deployment state
          --projectId TEXT Use to filter by project ID
          --modelId TEXT Use to filter by model ID

        :param state|projectId|modelId filters:
        """
        return repositories.ListDeployments(self.client).list(filters=filters)

    @staticmethod
    def _get_deployment_dict(deployment, schema_cls):
        deployment_schema = schema_cls()
        deployment_dict = deployment_schema.dump(deployment).data

        return deployment_dict

    @staticmethod
    def _get_error_message(response):
        try:
            response_data = response.json()
        except ValueError:
            return "Unknown error"

        msg = MessageExtractor().get_message_from_response_data(response_data)
        return msg

    def _get_create_response(self, deployment_dict):
        return self.client.post("/deployments/createDeployment/", json=deployment_dict)

    def _process_response(self, response):
        if response.ok:
            return response.json()["deployment"]["id"]

        msg = self._get_error_message(response)
        # TODO prepare more detailed error type message
        raise GradientSdkError(msg)

    def _create(self, deployment, schema_cls):
        deployment_dict = self._get_deployment_dict(deployment, schema_cls)
        response = self._get_create_response(deployment_dict)
        handle = self._process_response(response)
        return handle

    def _get_post_response(self, deployment_id, is_running=True):
        data = {
            "id": deployment_id,
            "isRunning": is_running
        }
        return self.client.post("/deployments/updateDeployment/", json=data)

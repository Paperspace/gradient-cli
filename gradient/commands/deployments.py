import abc
import pydoc

import six
import terminaltables
from halo import halo

from gradient import version, logger as gradient_logger, exceptions
from gradient.api_sdk import sdk_exceptions, utils, models
from gradient.api_sdk.clients import http_client
from gradient.api_sdk.config import config
from gradient.api_sdk.utils import urljoin
from gradient.commands.common import DetailsCommandMixin
from gradient.utils import get_terminal_lines

default_headers = {"X-API-Key": config.PAPERSPACE_API_KEY,
                   "ps_client_name": "gradient-cli",
                   "ps_client_version": version.version}
deployments_api = http_client.API(config.CONFIG_HOST, headers=default_headers)


@six.add_metaclass(abc.ABCMeta)
class _DeploymentCommand(object):
    def __init__(self, deployment_client, logger_=gradient_logger.Logger()):
        self.client = deployment_client
        self.logger = logger_

    @abc.abstractmethod
    def execute(self, **kwargs):
        pass


class CreateDeploymentCommand(_DeploymentCommand):
    def execute(self, use_vpc=False, **kwargs):
        self._handle_auth(kwargs)

        with halo.Halo(text="Creating new deployment", spinner="dots"):
            deployment_id = self.client.create(use_vpc=use_vpc, **kwargs)

        self.logger.log("New deployment created with id: {}".format(deployment_id))
        self.logger.log(self.get_instance_url(deployment_id))

    def get_instance_url(self, instance_id):
        url = urljoin(config.WEB_URL, "/console/deployments/{}".format(instance_id))
        return url

    def _handle_auth(self, kwargs):
        if kwargs.pop("generate_auth", False):
            auth_username, auth_password = utils.generate_credentials_pair(12)
            kwargs["auth_username"] = auth_username
            kwargs["auth_password"] = auth_password
            self.logger.log("Generated credentials: \nusername:{}\npassword:{}".format(auth_password, auth_username))


class ListDeploymentsCommand(_DeploymentCommand):
    WAITING_FOR_RESPONSE_MESSAGE = "Waiting for data..."

    def execute(self, use_vpc=False, **kwargs):
        with halo.Halo(text=self.WAITING_FOR_RESPONSE_MESSAGE, spinner="dots"):
            instances = self._get_instances(use_vpc=use_vpc, **kwargs)

        self._log_objects_list(instances)

    def _get_instances(self, use_vpc=False, **kwargs):
        try:
            instances = self.client.list(use_vpc=use_vpc, **kwargs)
        except sdk_exceptions.GradientSdkError as e:
            raise exceptions.ReceivingDataFailedError(e)

        return instances

    @staticmethod
    def _get_table_data(deployments):
        data = [("Name", "ID", "Endpoint", "Api Type", "Deployment Type", "Deployment State")]
        for deployment in deployments:
            name = deployment.name
            id_ = deployment.id
            endpoint = deployment.endpoint
            api_type = deployment.api_type
            deployment_type = deployment.deployment_type
            deployment_state = deployment.state
            data.append((name, id_, endpoint, api_type, deployment_type, deployment_state))

        return data

    def _log_objects_list(self, objects):
        if not objects:
            self.logger.warning("No data found")
            return

        table_data = self._get_table_data(objects)
        table_str = self._make_table(table_data)
        if len(table_str.splitlines()) > get_terminal_lines():
            pydoc.pager(table_str)
        else:
            self.logger.log(table_str)

    @staticmethod
    def _make_table(table_data):
        ascii_table = terminaltables.AsciiTable(table_data)
        table_string = ascii_table.table
        return table_string


class StartDeploymentCommand(_DeploymentCommand):
    def execute(self, use_vpc=False, **kwargs):
        self.client.start(use_vpc=use_vpc, **kwargs)
        self.logger.log("Deployment started")


class StopDeploymentCommand(_DeploymentCommand):
    def execute(self, use_vpc=False, **kwargs):
        self.client.stop(use_vpc=use_vpc, **kwargs)
        self.logger.log("Deployment stopped")


class DeleteDeploymentCommand(_DeploymentCommand):
    def execute(self, **kwargs):
        self.client.delete(**kwargs)
        self.logger.log("Deployment deleted")


class UpdateDeploymentCommand(_DeploymentCommand):
    def execute(self, deployment_id, use_vpc=False, **kwargs):
        with halo.Halo(text="Updating deployment data", spinner="dots"):
            self.client.update(deployment_id, use_vpc=use_vpc, **kwargs)

        self.logger.log("Deployment data updated")


class GetDeploymentDetails(DetailsCommandMixin, _DeploymentCommand):
    def _get_table_data(self, instance):
        """
        :param models.Deployment instance:
        """
        data = (
            ("ID", instance.id),
            ("Name", instance.name),
            ("State", instance.state),
            ("Machine type", instance.machine_type),
            ("Instance count", instance.instance_count),
            ("Deployment type", instance.deployment_type),
            ("Model ID", instance.model_id),
            ("Project ID", instance.project_id),
            ("Endpoint", instance.endpoint),
            ("API type", instance.api_type),
            ("Cluster ID", instance.cluster_id),
        )
        return data

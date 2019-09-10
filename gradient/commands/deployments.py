import abc
import pydoc

import six
import terminaltables
from halo import halo

from gradient import version, logger as gradient_logger, api_sdk, exceptions
from gradient.api_sdk.clients import http_client
from gradient.config import config
from gradient.utils import get_terminal_lines

default_headers = {"X-API-Key": config.PAPERSPACE_API_KEY,
                   "ps_client_name": "gradient-cli",
                   "ps_client_version": version.version}
deployments_api = http_client.API(config.CONFIG_HOST, headers=default_headers)


@six.add_metaclass(abc.ABCMeta)
class _DeploymentCommand(object):
    def __init__(self, deployment_client, logger_=gradient_logger.Logger()):
        self.deployment_client = deployment_client
        self.logger = logger_

    @abc.abstractmethod
    def execute(self, **kwargs):
        pass


class CreateDeploymentCommand(_DeploymentCommand):
    def execute(self, use_vpc=False, **kwargs):
        with halo.Halo(text="Creating new deployment", spinner="dots"):
            try:
                deployment_id = self.deployment_client.create(use_vpc=use_vpc, **kwargs)
            except api_sdk.GradientSdkError as e:
                self.logger.error(e)
            else:
                self.logger.log("New deployment created with id: {}".format(deployment_id))


class ListDeploymentsCommand(_DeploymentCommand):
    WAITING_FOR_RESPONSE_MESSAGE = "Waiting for data..."

    def execute(self, use_vpc=False, **kwargs):
        with halo.Halo(text=self.WAITING_FOR_RESPONSE_MESSAGE, spinner="dots"):
            instances = self._get_instances(use_vpc=use_vpc, **kwargs)

        self._log_objects_list(instances)

    def _get_instances(self, use_vpc=False, **kwargs):
        try:
            instances = self.deployment_client.list(use_vpc=use_vpc, **kwargs)
        except api_sdk.GradientSdkError as e:
            raise exceptions.ReceivingDataFailedError(e)

        return instances

    @staticmethod
    def _get_table_data(deployments):
        data = [("Name", "ID", "Endpoint", "Api Type", "Deployment Type", "Deployment State")]
        for deployment in deployments:
            name = deployment.name
            id_ = deployment.id_
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
        self.deployment_client.start(use_vpc=use_vpc, **kwargs)
        self.logger.log("Deployment started")


class StopDeploymentCommand(_DeploymentCommand):
    def execute(self, use_vpc=False, **kwargs):
        self.deployment_client.stop(use_vpc=use_vpc, **kwargs)
        self.logger.log("Deployment stopped")

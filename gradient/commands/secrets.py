import abc

import six

from gradient import api_sdk
from gradient.cli_constants import CLI_PS_CLIENT_NAME
from gradient.commands.common import BaseCommand, ListCommandMixin


@six.add_metaclass(abc.ABCMeta)
class BaseSecretsCommand(BaseCommand):
    def _get_client(self, api_key, logger):
        client = api_sdk.clients.SecretsClient(
            api_key=api_key,
            logger=logger,
            ps_client_name=CLI_PS_CLIENT_NAME,
        )
        return client


class ListSecretsCommand(ListCommandMixin, BaseSecretsCommand):
    def _get_instances(self, kwargs):
        instances = self.client.list(**kwargs)
        return instances

    def _get_table_data(self, objects):
        """
        :param list[Secret] objects: object
        """
        data = [("Name",)]
        for secret in objects:
            data.append((secret.name,))

        return data


class SetSecretCommand(BaseSecretsCommand):
    def execute(self, entity, entity_id, name, value):
        self.client.set(entity=entity, entity_id=entity_id, name=name, value=value)
        self.logger.log("Set {} secret '{}'".format(entity, name))


class DeleteSecretCommand(BaseSecretsCommand):
    def execute(self, entity, entity_id, name):
        self.client.delete(entity=entity, entity_id=entity_id, name=name)
        self.logger.log("Deleted {} secret '{}'".format(entity, name))
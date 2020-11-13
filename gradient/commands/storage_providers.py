import abc
import os

import six

from gradient import api_sdk
from gradient.cli_constants import CLI_PS_CLIENT_NAME
from gradient.commands.common import BaseCommand, DetailsCommandMixin, ListCommandPagerMixin


def format_config(config, limit=None):
    if not config:
        return ''

    values = []

    for i, (name, value) in enumerate(sorted(config.items())):
        if not isinstance(value, six.string_types + (int, float, bool)):
            continue

        if limit is not None and i >= limit:
            values.append('...')
            break

        values.append("{}: {}".format(name, value))

    return os.linesep.join(values)


@six.add_metaclass(abc.ABCMeta)
class BaseStorageProvidersCommand(BaseCommand):
    def _get_client(self, api_key, logger):
        client = api_sdk.clients.StorageProvidersClient(
            api_key=api_key,
            logger=logger,
            ps_client_name=CLI_PS_CLIENT_NAME,
        )
        return client


class ListStorageProvidersCommand(ListCommandPagerMixin, BaseStorageProvidersCommand):
    def _get_table_data(self, objects):
        data = [("Name", "ID", "Type", "Config")]
        for storage_provider in objects:
            data.append((
                storage_provider.name,
                storage_provider.id,
                storage_provider.type,
                format_config(storage_provider.config, limit=5)
            ))
        return data


class ShowStorageProviderDetailsCommand(DetailsCommandMixin, BaseStorageProvidersCommand):
    def _get_table_data(self, instance):
        data = (
            ("Name", instance.name),
            ("ID", instance.id),
            ("Type", instance.type),
            ("Config", format_config(instance.config))
        )
        return data


class CreateS3StorageProviderCommand(BaseStorageProvidersCommand):
    def execute(self, name, bucket, access_key, secret_access_key, endpoint=None, region=None, signature_version=None):
        storage_provider_id = self.client.create_s3(
            name=name,
            bucket=bucket,
            access_key=access_key,
            secret_access_key=secret_access_key,
            endpoint=endpoint,
            region=region,
            signature_version=signature_version,
        )
        self.logger.log("Created new storage provider with id: {}".format(storage_provider_id))


class UpdateS3StorageProviderCommand(BaseStorageProvidersCommand):
    def execute(self, storage_provider_id, name=None, bucket=None, access_key=None, secret_access_key=None,
                endpoint=None, region=None, signature_version=None):
        self.client.update_s3(
            storage_provider_id=storage_provider_id,
            name=name,
            bucket=bucket,
            access_key=access_key,
            secret_access_key=secret_access_key,
            endpoint=endpoint,
            region=region,
            signature_version=signature_version,
        )
        self.logger.log("Updated storage provider")


class DeleteStorageProviderCommand(BaseStorageProvidersCommand):
    def execute(self, storage_provider_id):
        self.client.delete(storage_provider_id)
        self.logger.log("Deleted storage provider: {}".format(storage_provider_id))

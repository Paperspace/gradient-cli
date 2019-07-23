import abc

import six

from gradient import api_sdk, exceptions
from gradient.commands.common import BaseCommand, ListCommandMixin


@six.add_metaclass(abc.ABCMeta)
class BaseModelCommand(BaseCommand):
    def _get_client(self, api_key, logger):
        client = api_sdk.clients.ModelsClient(api_key=api_key, logger=logger)
        return client


class ListModelsCommand(ListCommandMixin, BaseModelCommand):
    def _get_instances(self, kwargs):
        try:
            instances = self.client.list(**kwargs)
        except api_sdk.GradientSdkError as e:
            raise exceptions.ReceivingDataFailedError(e)

        return instances

    def _get_table_data(self, models):
        data = [("Name", "ID", "Model Type", "Project ID", "Experiment ID")]
        for model in models:
            name = model.name
            id_ = model.id
            project_id = model.project_id
            experiment_id = model.experiment_id
            model_type = model.model_type
            data.append((name, id_, model_type, project_id, experiment_id))

        return data

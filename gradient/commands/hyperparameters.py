import abc

import six

from gradient import api_sdk, exceptions
from gradient.api_sdk import sdk_exceptions
from gradient.cli_constants import CLI_PS_CLIENT_NAME
from gradient.commands.common import BaseCommand, ListCommandMixin, DetailsCommandMixin
from gradient.commands.experiments import BaseCreateExperimentCommandMixin


@six.add_metaclass(abc.ABCMeta)
class BaseHyperparameterCommand(BaseCommand):
    def _get_client(self, api_key, logger):
        client = api_sdk.clients.HyperparameterJobsClient(
            api_key=api_key,
            logger=logger,
            ps_client_name=CLI_PS_CLIENT_NAME,
        )
        return client


class CreateHyperparameterCommand(BaseCreateExperimentCommandMixin, BaseHyperparameterCommand):
    SPINNER_MESSAGE = "Creating hyperparameter tuning job"
    CREATE_SUCCESS_MESSAGE_TEMPLATE = "Hyperparameter tuning job created with ID: {}"

    def _create(self, hyperparameter):
        handle = self.client.create(**hyperparameter)
        return handle


class CreateAndStartHyperparameterCommand(BaseCreateExperimentCommandMixin, BaseHyperparameterCommand):
    SPINNER_MESSAGE = "Creating and starting hyperparameter tuning job"
    CREATE_SUCCESS_MESSAGE_TEMPLATE = "Hyperparameter tuning job created and started with ID: {}"

    def _create(self, hyperparameter):
        handle = self.client.run(**hyperparameter)
        return handle


class ListHyperparametersCommand(ListCommandMixin, BaseHyperparameterCommand):
    def _get_instances(self, kwargs):
        try:
            instances = self.client.list()
        except sdk_exceptions.GradientSdkError as e:
            raise exceptions.ReceivingDataFailedError(e)

        return instances

    def _get_table_data(self, objects):
        data = [("Name", "ID", "Project ID")]
        for obj in objects:
            data.append((obj.name, obj.id, obj.project_id))
        return data


class HyperparameterDetailsCommand(DetailsCommandMixin, BaseHyperparameterCommand):
    WAITING_FOR_RESPONSE_MESSAGE = "Waiting for data..."

    def _get_table_data(self, instance):
        """
        :param api_sdk.Hyperparameter instance:
        """
        data = (
            ("ID", instance.id),
            ("Name", instance.name),
            ("Ports", instance.ports),
            ("Project ID", instance.project_id),
            ("Tuning command", instance.tuning_command),
            ("Worker command", instance.worker_command),
            ("Worker container", instance.worker_container),
            ("Worker count", instance.worker_count),
            ("Worker machine type", instance.worker_machine_type),
            ("Worker use dockerfile", instance.use_dockerfile or False),
            ("Workspace URL", instance.workspace_url),
        )
        return data


class HyperparameterStartCommand(BaseHyperparameterCommand):
    def execute(self, id_):
        self.client.start(id_)
        self.logger.log("Hyperparameter tuning started")


class HyperparameterAddTagsCommand(BaseHyperparameterCommand):
    def execute(self, hyperparameter_id, *args, **kwargs):
        self.client.add_tags(hyperparameter_id, **kwargs)
        self.logger.log("Tags added to hyperparameter")


class HyperparameterRemoveTagsCommand(BaseHyperparameterCommand):
    def execute(self, hyperparameter_id, *args, **kwargs):
        self.client.remove_tags(hyperparameter_id, **kwargs)
        self.logger.log("Tags removed from hyperparameter")

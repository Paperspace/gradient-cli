import abc

import halo
import six

from gradient import api_sdk, exceptions, cli_constants
from gradient.api_sdk import sdk_exceptions
from gradient.api_sdk.s3_downloader import ModelFilesDownloader
from gradient.commands.common import BaseCommand, ListCommandMixin, DetailsCommandMixin
from gradient.exceptions import ApplicationError


@six.add_metaclass(abc.ABCMeta)
class GetModelsClientMixin:
    def _get_client(self, api_key, logger):
        client = api_sdk.clients.ModelsClient(
            api_key=api_key,
            logger=logger,
            ps_client_name=cli_constants.CLI_PS_CLIENT_NAME,
        )
        return client


class ListModelsCommand(GetModelsClientMixin, ListCommandMixin, BaseCommand):
    def _get_instances(self, kwargs):
        try:
            instances = self.client.list(**kwargs)
        except sdk_exceptions.GradientSdkError as e:
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


class DeleteModelCommand(GetModelsClientMixin, BaseCommand):
    def execute(self, model_id, *args, **kwargs):
        self.client.delete(model_id)
        self.logger.log("Model deleted")


class UploadModel(GetModelsClientMixin, BaseCommand):
    SPINNER_MESSAGE = "Uploading model"

    def execute(self, **kwargs):
        with halo.Halo(text=self.SPINNER_MESSAGE, spinner="dots"):
            model_id = self.client.upload(**kwargs)

        self.logger.log("Model uploaded with ID: {}".format(model_id))


class GetModelCommand(DetailsCommandMixin, GetModelsClientMixin, BaseCommand):
    def _get_table_data(self, instance):
        """
        :param api_sdk.Model instance:
        """
        tags_string = ", ".join(instance.tags)

        data = (
            ("ID", instance.id),
            ("Name", instance.name),
            ("Project ID", instance.project_id),
            ("Experiment ID", instance.experiment_id),
            ("Model Type", instance.model_type),
            ("URL", instance.url),
            ("Deployment State", instance.deployment_state),
            ("Tags", tags_string),
        )
        return data


class DownloadModelFiles(GetModelsClientMixin, BaseCommand):
    WAITING_FOR_RESPONSE_MESSAGE = "Downloading files..."

    def execute(self, model_id, destination_directory):
        model_files_downloader = ModelFilesDownloader(
            self.api_key,
            logger=self.logger,
            ps_client_name=cli_constants.CLI_PS_CLIENT_NAME,
        )
        try:
            model_files_downloader.download(model_id, destination_directory)
        except OSError as e:
            raise ApplicationError(e)


class MLModelAddTagsCommand(GetModelsClientMixin, BaseCommand):
    def execute(self, ml_model_id, *args, **kwargs):
        self.client.add_tags(ml_model_id, **kwargs)
        self.logger.log("Tags added to ml model")


class MLModelRemoveTagsCommand(GetModelsClientMixin, BaseCommand):
    def execute(self, ml_model_id, *args, **kwargs):
        self.client.remove_tags(ml_model_id, **kwargs)
        self.logger.log("Tags removed from ml model")

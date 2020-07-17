import abc

import halo
import six

from gradient import api_sdk, exceptions
from gradient.api_sdk import sdk_exceptions
from gradient.api_sdk.config import config
from gradient.api_sdk.utils import concatenate_urls
from gradient.cli_constants import CLI_PS_CLIENT_NAME
from .common import BaseCommand, ListCommandMixin, DetailsCommandMixin


@six.add_metaclass(abc.ABCMeta)
class BaseProjectCommand(BaseCommand):
    def _get_client(self, api_key, logger):
        client = api_sdk.clients.ProjectsClient(
            api_key=api_key,
            logger=logger,
            ps_client_name=CLI_PS_CLIENT_NAME,
        )
        return client


class CreateProjectCommand(BaseProjectCommand):
    SPINNER_MESSAGE = "Creating new project"
    CREATE_SUCCESS_MESSAGE_TEMPLATE = "Project created with ID: {}"

    def execute(self, project_dict):
        with halo.Halo(text=self.SPINNER_MESSAGE, spinner="dots"):
            project_id = self.client.create(**project_dict)

        self.logger.log(self.CREATE_SUCCESS_MESSAGE_TEMPLATE.format(project_id))
        self.logger.log(self.get_instance_url(project_id))

    def get_instance_url(self, project_id):
        url = concatenate_urls(config.WEB_URL, "projects/{}".format(project_id))
        return url


class ListProjectsCommand(ListCommandMixin, BaseProjectCommand):
    def _get_instances(self, kwargs):
        try:
            instances = self.client.list(**kwargs)
        except sdk_exceptions.GradientSdkError as e:
            raise exceptions.ReceivingDataFailedError(e)

        return instances

    def _get_table_data(self, objects):
        data = [("ID", "Name", "Repository", "Created")]
        for obj in objects:
            created_str = obj.created.strftime("%Y-%m-%d %H:%M:%S.%f")
            data.append((obj.id, obj.name, obj.repository_url, created_str))

        return data


class DeleteProjectCommand(BaseProjectCommand):
    def execute(self, project_id):
        self.client.delete(project_id)
        self.logger.log("Project deleted")


class ProjectAddTagsCommand(BaseProjectCommand):
    def execute(self, project_id, *args, **kwargs):
        self.client.add_tags(project_id, **kwargs)
        self.logger.log("Tags added to project")


class ProjectRemoveTagsCommand(BaseProjectCommand):
    def execute(self, project_id, *args, **kwargs):
        self.client.remove_tags(project_id, **kwargs)
        self.logger.log("Tags removed from project")


class ShowProjectDetailsCommand(DetailsCommandMixin, BaseProjectCommand):
    def _get_table_data(self, instance):
        """
        :param api_sdk.Project instance:
        """
        tags_string = ", ".join(instance.tags)

        data = (
            ("Name", instance.name),
            ("ID", instance.id),
            ("Repository name", instance.repository_name),
            ("Repository url", instance.repository_url),
            ("Tags", tags_string),
        )
        return data

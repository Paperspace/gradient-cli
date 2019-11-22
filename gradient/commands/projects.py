import abc

import halo
import six

from gradient import api_sdk, exceptions
from gradient.api_sdk import sdk_exceptions
from gradient.api_sdk.config import config
from gradient.api_sdk.utils import urljoin
from .common import BaseCommand, ListCommandMixin


@six.add_metaclass(abc.ABCMeta)
class BaseProjectCommand(BaseCommand):
    def _get_client(self, api_key, logger):
        client = api_sdk.clients.ProjectsClient(api_key=api_key, logger=logger)
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
        url = urljoin(config.WEB_URL, "console/projects/{}/machines".format(project_id))
        return url


class ListProjectsCommand(ListCommandMixin, BaseProjectCommand):
    def _get_instances(self, kwargs):
        try:
            instances = self.client.list()
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

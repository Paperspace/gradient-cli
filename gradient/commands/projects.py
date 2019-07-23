import abc

import halo
import six

from gradient import api_sdk, exceptions
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
            try:
                project_id = self.client.create(**project_dict)
            except api_sdk.GradientSdkError as e:
                self.logger.error(e)
                return

        self.logger.log(self.CREATE_SUCCESS_MESSAGE_TEMPLATE.format(project_id))


class ListProjectsCommand(ListCommandMixin, BaseProjectCommand):
    def _get_instances(self, kwargs):
        try:
            instances = self.client.list()
        except api_sdk.GradientSdkError as e:
            raise exceptions.ReceivingDataFailedError(e)

        return instances

    def _get_table_data(self, objects):
        data = [("ID", "Name", "Repository", "Created")]
        for obj in objects:
            data.append((obj.id, obj.name, obj.repository_url, obj.created))

        return data

import abc

import halo
import six

from gradient import api_sdk
from . import common
from .common import BaseCommand, ListCommand


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


class ListProjectsCommand(ListCommand):
    @property
    def request_url(self):
        return "/projects/"

    def _get_request_json(self, kwargs):
        # TODO: PS_API should not require teamId but it does now, delete teamId from json when PS_API is fixed
        return {"teamId": 666}

    def _get_objects(self, response, kwargs):
        data = super(ListProjectsCommand, self)._get_objects(response, kwargs)
        objects = data["data"]
        return objects

    def _get_table_data(self, projects):
        data = [("ID", "Name", "Repository", "Created")]
        for project in projects:
            id_ = project.get("handle")
            name = project.get("name")
            repo_url = project.get("repoUrl")
            created = project.get("dtCreated")
            data.append((id_, name, repo_url, created))

        return data


class ProjectCommandBase(common.CommandBase):
    def _log_message(self, response, success_msg_template, error_msg):
        if response.ok:
            try:
                j = response.json()
            except (ValueError, KeyError):
                self.logger.error(success_msg_template)
            else:
                msg = success_msg_template.format(**j)
                self.logger.log(msg)
        else:
            try:
                data = response.json()
                self.logger.log_error_response(data)
            except ValueError:
                self.logger.error(error_msg)

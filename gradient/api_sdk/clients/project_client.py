from gradient.api_sdk import models, repositories

from gradient.config import config
from .base_client import BaseClient


class ProjectsClient(BaseClient):
    HOST_URL = config.CONFIG_HOST

    def create(self, name, repository_name=None, repository_url=None):
        """Create new project

        :param str name:
        :param str repository_name:
        :param str repository_url:

        :returns: project ID
        :rtype: str
        """

        project = models.Project(
            name=name,
            repository_name=repository_name,
            repository_url=repository_url,
        )

        handle = repositories.CreateProject(self.client).create(project)
        return handle

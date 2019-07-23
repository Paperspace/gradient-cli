from gradient.config import config
from .base_client import BaseClient
from .. import models, repositories


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

    def list(self):
        """Get list of projects

        :returns: list of projects
        :rtype: list[models.Project]
        """
        projects = repositories.ListProjects(self.client).list()
        return projects

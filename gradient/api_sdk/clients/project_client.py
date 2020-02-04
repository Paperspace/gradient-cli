from .base_client import BaseClient
from .tag_client import TagClient
from .. import models, repositories


class ProjectsClient(BaseClient):
    entity = "project"

    def create(self, name, repository_name=None, repository_url=None, tags=None,):
        """Create new project

        *EXAMPLE*::

            gradient projects create --name new-project

        *EXAMPLE RETURN*::

            Project created with ID: <your-project-id>


        in sdk::

            from gradient.api_sdk.clients import ProjectsClient

            api_key = 'your-api-key'
            projects_client = ProjectsClient(api_key)

            new_project = projects_client.create('your-project-name')

            print(new_project)

        :param str name: Name of new project [required]
        :param str repository_name: Name of the repository
        :param str repository_url: URL to the repository
        :param list[str] tags: List of tags

        :returns: project ID
        :rtype: str
        """

        project = models.Project(
            name=name,
            repository_name=repository_name,
            repository_url=repository_url,
        )

        handle = repositories.CreateProject(api_key=self.api_key, logger=self.logger).create(project)
        if tags:
            self.add_tags(entity_id=handle, tags=tags)
        return handle

    def list(self, tags=None):
        """Get list of your projects

        :param list[str]|tuple[str] tags: tags to filter with OR

        :returns: list of projects
        :rtype: list[models.Project]
        """

        projects = repositories.ListProjects(api_key=self.api_key, logger=self.logger).list(tags=tags)
        return projects

    def delete(self, project_id):
        repository = repositories.DeleteProject(api_key=self.api_key, logger=self.logger)
        repository.delete(project_id)

    def add_tags(self, entity_id, tags):
        tag_client = TagClient(api_key=self.api_key)
        tag_client.add_tags(entity_id=entity_id, entity=self.entity, tags=tags)

    def remove_tags(self, entity_id, tags):
        tag_client = TagClient(api_key=self.api_key)
        tag_client.remove_tags(entity_id=entity_id, entity=self.entity, tags=tags)

from .base_client import BaseClient
from .. import models, repositories


class ProjectsClient(BaseClient):
    entity = "project"

    def create(self, name, repository_name=None, repository_url=None, tags=None, ):
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

        repository = self.build_repository(repositories.CreateProject)
        handle = repository.create(project)

        if tags:
            self.add_tags(entity_id=handle, entity=self.entity, tags=tags)

        return handle

    def list(self, tags=None):
        """Get list of your projects

        :param list[str]|tuple[str] tags: tags to filter with OR

        :returns: list of projects
        :rtype: list[models.Project]
        """

        repository = self.build_repository(repositories.ListProjects)
        projects = repository.list(tags=tags)
        return projects

    def delete(self, project_id):
        repository = self.build_repository(repositories.DeleteProject)
        repository.delete(project_id)

    def get(self, project_id):
        repository = self.build_repository(repositories.GetProject)
        project = repository.get(id=project_id)
        return project

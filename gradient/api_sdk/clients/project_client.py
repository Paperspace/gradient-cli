from .base_client import BaseClient
from .. import models, repositories


class ProjectsClient(BaseClient):
    def create(self, name, repository_name=None, repository_url=None):
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

        :returns: project ID
        :rtype: str
        """

        project = models.Project(
            name=name,
            repository_name=repository_name,
            repository_url=repository_url,
        )

        handle = repositories.CreateProject(api_key=self.api_key, logger=self.logger).create(project)
        return handle

    def list(self):
        """Get list of your projects

        *EXAMPLE*::

            gradient projects list

        *EXAMPLE RETURN*::

            +-----------+------------------+------------+----------------------------+
            | ID        | Name             | Repository | Created                    |
            +-----------+------------------+------------+----------------------------+
            | project-id| <name-of-project>| None       | 2019-06-28 10:38:57.874000 |
            | project-id| <name-of-project>| None       | 2019-07-17 13:17:34.493000 |
            | project-id| <name-of-project>| None       | 2019-07-17 13:21:12.770000 |
            | project-id| <name-of-project>| None       | 2019-07-29 09:26:49.105000 |
            +-----------+------------------+------------+----------------------------+

        in sdk::

            from gradient.api_sdk.clients import ProjectsClient

            api_key = 'your-api-key'
            projects_client = ProjectsClient(api_key)

            projects_list = projects_client.list()

            for project in project_list:
                print(project)


        :returns: list of projects
        :rtype: list[models.Project]
        """

        projects = repositories.ListProjects(api_key=self.api_key, logger=self.logger).list()
        return projects

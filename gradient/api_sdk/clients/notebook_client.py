from .base_client import BaseClient
from .. import repositories, models


class NotebooksClient(BaseClient):
    def create(
            self,
            vm_type_id,
            container_id,
            cluster_id,
            container_name=None,
            name=None,
            registry_username=None,
            registry_password=None,
            default_entrypoint=None,
            container_user=None,
            shutdown_timeout=None,
            is_preemptible=None,
    ):
        """Create new notebook

        :param int vm_type_id:
        :param int container_id:
        :param int cluster_id:
        :param str container_name:
        :param str name:
        :param str registry_username:
        :param str registry_password:
        :param str default_entrypoint:
        :param str container_user:
        :param int|float shutdown_timeout:
        :param bool is_preemptible:

        :return: Notebook ID
        :rtype str:
        """

        notebook = models.Notebook(
            vm_type_id=vm_type_id,
            container_id=container_id,
            cluster_id=cluster_id,
            container_name=container_name,
            name=name,
            registry_username=registry_username,
            registry_password=registry_password,
            default_entrypoint=default_entrypoint,
            container_user=container_user,
            shutdown_timeout=shutdown_timeout,
            is_preemptible=is_preemptible,
        )

        repository = repositories.CreateNotebook(api_key=self.api_key, logger=self.logger)
        handle = repository.create(notebook)
        return handle

    def get(self, id):
        """Get Notebook

        :param str id: Notebook ID
        :rtype: models.Notebook
        """
        repository = repositories.GetNotebook(api_key=self.api_key, logger=self.logger)
        notebook = repository.get(id=id)
        return notebook

    def delete(self, id):
        """Delete existing notebook

        :param str id: Notebook ID
        """
        repository = repositories.DeleteNotebook(api_key=self.api_key, logger=self.logger)
        repository.delete(id)

    def list(self):
        """Get list of Notebooks

        :rtype: list[models.Notebook]
        """
        repository = repositories.ListNotebooks(api_key=self.api_key, logger=self.logger)
        notebooks = repository.list()
        return notebooks

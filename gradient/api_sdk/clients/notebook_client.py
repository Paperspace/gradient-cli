from .base_client import BaseClient
from .. import repositories, models


class NotebooksClient(BaseClient):
    def create(
            self,
            vp_type_id,
            container_id,
            container_name=None,
            name=None,
            cluster_id=None,
            registry_username=None,
            registry_password=None,
            default_entrypoint=None,
            container_user=None,
            shutdown_timeout=None,
            is_preemptible=None,
    ):
        """Create new notebook

        :param str vp_type_id:
        :param str container_id:
        :param str container_name:
        :param str name:
        :param str cluster_id:
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
            vp_type_id=vp_type_id,
            container_id=container_id,
            container_name=container_name,
            name=name,
            cluster_id=cluster_id,
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

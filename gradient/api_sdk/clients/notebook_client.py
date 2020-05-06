from .base_client import BaseClient
from .. import repositories, models


class NotebooksClient(BaseClient):
    entity = "notebook"

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
            tags=None,
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
        :param list[str] tags: List of tags

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

        repository = self.build_repository(repositories.CreateNotebook)
        handle = repository.create(notebook)

        if tags:
            self.add_tags(entity_id=handle, entity=self.entity, tags=tags)

        return handle

    def get(self, id):
        """Get Notebook

        :param str id: Notebook ID
        :rtype: models.Notebook
        """
        repository = self.build_repository(repositories.GetNotebook)
        notebook = repository.get(id=id)
        return notebook

    def delete(self, id):
        """Delete existing notebook

        :param str id: Notebook ID
        """
        repository = self.build_repository(repositories.DeleteNotebook)
        repository.delete(id)

    def list(self, tags=None, limit=None, offset=None, get_meta=False):
        """Get list of Notebooks

        :rtype: list[models.Notebook]
        """
        repository = self.build_repository(repositories.ListNotebooks)
        notebooks = repository.list(tags=tags, limit=limit, offset=offset, get_meta=get_meta)
        return notebooks

    def get_metrics(self, notebook_id, start=None, end=None, interval="30s", built_in_metrics=None):
        """Get notebook metrics

        :param str notebook_id: notebook ID
        :param datetime.datetime|str start:
        :param datetime.datetime|str end:
        :param str interval:
        :param list[str] built_in_metrics: List of metrics to get if different than default
                    Available builtin metrics: cpuPercentage, memoryUsage, gpuMemoryFree, gpuMemoryUsed, gpuPowerDraw,
                                            gpuTemp, gpuUtilization, gpuMemoryUtilization

        :returns: Metrics of a notebook
        :rtype: dict[str,dict[str,list[dict]]]
        """

        repository = self.build_repository(repositories.GetNotebookMetrics)
        metrics = repository.get(
            id=notebook_id,
            start=start,
            end=end,
            interval=interval,
            built_in_metrics=built_in_metrics,
        )
        return metrics

    def stream_metrics(self, notebook_id, interval="30s", built_in_metrics=None):
        """Stream live notebook metrics

        :param str notebook_id: notebook ID
        :param str interval:
        :param list[str] built_in_metrics: List of metrics to get if different than default
                    Available builtin metrics: cpuPercentage, memoryUsage, gpuMemoryFree, gpuMemoryUsed, gpuPowerDraw,
                                            gpuTemp, gpuUtilization, gpuMemoryUtilization

        :returns: Generator object yielding live notebook metrics
        :rtype: Iterable[dict]
        """

        repository = self.build_repository(repositories.StreamNotebookMetrics)
        metrics = repository.stream(
            id=notebook_id,
            interval=interval,
            built_in_metrics=built_in_metrics,
        )
        return metrics

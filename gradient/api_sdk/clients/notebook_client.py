from .base_client import BaseClient, TagsSupportMixin
from .. import repositories, models


class NotebooksClient(TagsSupportMixin, BaseClient):
    entity = "notebook"

    def create(
            self,
            machine_type,
            project_id=None,
            cluster_id=None,
            container=None,
            container_id=None,
            name=None,
            registry_username=None,
            registry_password=None,
            command=None,
            container_user=None,
            shutdown_timeout=None,
            is_preemptible=None,
            is_public=None,
            workspace=None,
            workspace_ref=None,
            workspace_username=None,
            workspace_password=None,
            tags=None,
            environment=None,
    ):
        """Create new notebook

        :param str machine_type:
        :param int container_id:
        :param str|int project_id:
        :param str cluster_id:
        :param str container:
        :param str name:
        :param str registry_username:
        :param str registry_password:
        :param str command:
        :param str container_user:
        :param int shutdown_timeout:
        :param bool is_preemptible:
        :param bool is_public:
        :param list[str] tags: List of tags
        :param str workspace: Project git repository url
        :param str workspace_ref: Git commit hash, branch name or tag
        :param str workspace_username: Project git repository username
        :param str workspace_password: Project git repository password
        :param dict environment: key value collection of envs that are used in notebook

        :return: Notebook ID
        :rtype str:
        """

        notebook = models.Notebook(
            container_id=container_id,
            project_id=project_id,
            cluster_id=cluster_id,
            container=container,
            name=name,
            registry_username=registry_username,
            registry_password=registry_password,
            command=command,
            container_user=container_user,
            shutdown_timeout=shutdown_timeout,
            is_preemptible=is_preemptible,
            machine_type=machine_type,
            is_public=is_public,
            environment=environment,
            workspace=workspace,
            workspace_username=workspace_username,
            workspace_password=workspace_password,
            workspace_ref=workspace_ref,
        )

        repository = self.build_repository(repositories.CreateNotebook)
        handle = repository.create(notebook)

        if tags:
            self.add_tags(entity_id=handle, tags=tags)

        return handle

    def start(
            self,
            id,
            machine_type,
            cluster_id=None,
            name=None,
            shutdown_timeout=None,
            is_preemptible=None,
            tags=None,
    ):
        """Start existing notebook
        :param str|int id:
        :param str machine_type:
        :param str cluster_id:
        :param str name:
        :param int shutdown_timeout:
        :param bool is_preemptible:
        :param list[str] tags: List of tags

        :return: Notebook ID
        :rtype str:
        """
        notebook = models.NotebookStart(
            notebook_id=id,
            machine_type=machine_type,
            cluster_id=cluster_id,
            notebook_name=name,
            shutdown_timeout=shutdown_timeout,
            is_preemptible=is_preemptible,
        )

        repository = self.build_repository(repositories.StartNotebook)

        handle = repository.start(notebook)

        if tags:
            self.add_tags(entity_id=handle, tags=tags)

        return handle

    def fork(self, id, project_id, tags=None):
        """Fork an existing notebook
        :param str|int id:
        :param str project_id:
        :param list[str] tags: List of tags

        :return: Notebook ID
        :rtype str:
        """
        repository = self.build_repository(repositories.ForkNotebook)
        handle = repository.fork(id, project_id)

        if tags:
            self.add_tags(entity_id=handle, tags=tags)

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

    def stop(self, id):
        """Stop existing notebook

        :param str|int id: Notebook ID
        """
        repository = self.build_repository(repositories.StopNotebook)
        repository.stop(id)

    def artifacts_list(self, notebook_id, files=None, size=False, links=True):
        """
        Method to retrieve all artifacts files.

        .. code-block:: python
            :linenos:
            :emphasize-lines: 2

            artifacts = notebook_client.artifacts_list(
                notebook_id='your_notebook_id_here',
                files='your_files,here',
                size=False,
                links=True
            )

        :param str notebook_id: to limit artifact from this notebook.
        :param str files: to limit result only to file names provided. You can use wildcard option ``*``.
        :param bool size: flag to show file size. Default value is set to False.
        :param bool links: flag to show file url. Default value is set to True.

        :returns: list of files with description if specified from notebook artifacts.
        :rtype: list[Artifact]
        """
        repository = self.build_repository(repositories.ListNotebookArtifacts)
        artifacts = repository.list(notebook_id=notebook_id, files=files, links=links, size=size)
        return artifacts

    def logs(self, notebook_id, line=1, limit=10000):
        """
        Method to retrieve notebook logs.

        .. code-block:: python
            :linenos:
            :emphasize-lines: 2

            notebook_logs = notebook_client.logs(
                notebook_id='Your_job_id_here',
                line=100,
                limit=100
            )

        :param str notebook_id: id of notebook that we want to retrieve logs
        :param int line: from what line you want to retrieve logs. Default 0
        :param int limit: how much lines you want to retrieve logs. Default 10000

        :returns: list of formatted logs lines
        :rtype: list
        """
        notebook = self.get(notebook_id)
        repository = self.build_repository(repositories.ListNotebookLogs)
        logs = repository.list(job_id=notebook.job_handle, notebook_id=notebook_id, line=line, limit=limit)
        return logs

    def yield_logs(self, notebook_id, line=1, limit=10000):
        """Get log generator. Polls the API for new logs

        .. code-block:: python
            :linenos:
            :emphasize-lines: 2

            notebook_logs_generator = notebook_client.yield_logs(
                notebook_id='Your_job_id_here',
                line=100,
                limit=100
            )

        :param str notebook_id:
        :param int line: line number at which logs starts to display on screen
        :param int limit: maximum lines displayed on screen, default set to 10 000

        :returns: generator yielding LogRow instances
        :rtype: Iterator[models.LogRow]
        """

        notebook = self.get(notebook_id)
        repository = self.build_repository(repositories.ListNotebookLogs)
        logs = repository.yield_logs(job_id=notebook.job_handle, notebook_id=notebook_id, line=line, limit=limit)
        return logs

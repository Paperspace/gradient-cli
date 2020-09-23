"""
Jobs related client handler logic.

Remember that in code snippets all highlighted lines are required other lines are optional.
"""
from .base_client import BaseClient, TagsSupportMixin
from ..models import Artifact, Job
from ..repositories.jobs import ListJobs, ListJobLogs, ListJobArtifacts, CreateJob, DeleteJob, StopJob, \
    DeleteJobArtifacts, GetJobArtifacts, GetJobMetrics, StreamJobMetrics


class JobsClient(TagsSupportMixin, BaseClient):
    """
    Client to handle job related actions.

    How to create instance of job client:

    .. code-block:: python
        :linenos:
        :emphasize-lines: 4

        from gradient import JobsClient

        job_client = JobClient(
            api_key='your_api_key_here'
        )

    """
    entity = "job"

    def create(
            self,
            machine_type,
            container,
            project_id,
            data=None,
            name=None,
            command=None,
            ports=None,
            is_public=None,
            working_directory=None,
            experiment_id=None,
            job_env=None,
            use_dockerfile=None,
            is_preemptible=None,
            project=None,
            started_by_user_id=None,
            rel_dockerfile_path=None,
            registry_username=None,
            registry_password=None,
            cluster=None,
            cluster_id=None,
            node_attrs=None,
            workspace_file_name=None,
            registry_target=None,
            registry_target_username=None,
            registry_target_password=None,
            build_only=False,
            tags=None,
    ):
        """
        Method to create and start job in paperspace gradient.

        Example create job:

        .. code-block:: python
            :linenos:
            :emphasize-lines: 2,3,4

            job = job_client.create(
                machine_type='K80',
                container='tensorflow/tensorflow:1.13.1-gpu-py3',
                project_id='Som3ProjecTiD',
                data=data,
                name='Example job',
                command='pip install -r requirements.txt && python mnist.py',
                ports='5000:5000',
                job_env={
                    'CUSTOM_ENV'='Some value that will be set as system environment',
                }
            )

        :param str machine_type: Type of machine on which job should run. This field is **required**.

            We recommend to choose one of this:

            .. code-block::

                K80
                P100
                TPU
                GV100
                GV100x8
                G1
                G6
                G12

        :param str container: name of docker container that should be used to run job. This field is **required**.

            Example value: ``tensorflow/tensorflow:1.13.1-gpu-py3``

        :param str project_id: Identify to which project job should be connected. This field is **required**.

        :param None|MultipartEncoderMonitor data: None if there are no data to upload or
            encoded multipart data information with files to upload.
        :param str name: name for job that creator wish to have. If not provided it will be autogenerated.
        :param str command: custom command that should be run against command from docker image
        :param str ports: string with comma `,` separated mapped ports.

            Example value: ``5000:5000,8080:8080``

        :param bool is_public: bool flag to select if job should be available by default None
        :param str working_directory: location of code to run. By default ``/paperspace``
        :param str experiment_id: Id of experiment to which job should be connected. If not provided there will be
            created new experiment for this job.
        :param dict job_env: key value collection of envs that are used in code
        :param bool use_dockerfile: determines whether to build from Dockerfile (default false).
            Do not include a --container argument when using this flag.
        :param bool is_preemptible: flag if we you want to use spot instance. By default False
        :param str project: name of project that job is linked to.
        :param str started_by_user_id: id of user that started job. By default it take user id from access token
            or api key.
        :param str rel_dockerfile_path: relative location to your dockerfile. Default set to ``./Dockerfile``
        :param str registry_username: username for custom docker registry
        :param str registry_password: password for custom docker registry
        :param str cluster: name of cluster that job should be run on.
        :param str cluster_id: id of cluster that job should be run on. If you use one of recommended machine type
            cluster will be chosen so you do not need to provide it.
        :param dict node_attrs:
        :param str workspace_file_name:
        :param str registry_target: custom docker registry
        :param str registry_target_username: username for custom docker registry
        :param str registry_target_password: password for custom docker registry
        :param bool build_only: determines whether to only build and not run image
        :param list[str] tags: List of tags

        :returns: Job handle
        :rtype: str
        """

        if not build_only:
            build_only = None

        job = Job(
            machine_type=machine_type,
            container=container,
            project_id=project_id,
            name=name,
            command=command,
            ports=ports,
            is_public=is_public,
            working_directory=working_directory,
            experiment_id=experiment_id,
            job_env=job_env,
            use_dockerfile=use_dockerfile,
            is_preemptible=is_preemptible,
            project=project,
            started_by_user_id=started_by_user_id,
            rel_dockerfile_path=rel_dockerfile_path,
            registry_username=registry_username,
            registry_password=registry_password,
            cluster=cluster,
            cluster_id=cluster_id,
            target_node_attrs=node_attrs,
            workspace_file_name=workspace_file_name,
            registry_target=registry_target,
            registry_target_username=registry_target_username,
            registry_target_password=registry_target_password,
            build_only=build_only,
        )
        repository = self.build_repository(CreateJob)
        handle = repository.create(job, data=data)

        if tags:
            self.add_tags(entity_id=handle, tags=tags)

        return handle

    def delete(self, job_id):
        """
        Method to remove job.

        .. code-block:: python
            :linenos:
            :emphasize-lines: 2

            job_client.delete(
                job_id='Your_job_id_here'
            )

        :param str job_id: id of job that you want to remove
        :raises: exceptions.GradientSdkError
        """
        repository = self.build_repository(DeleteJob)
        repository.delete(job_id)

    def stop(self, job_id):
        """
        Method to stop working job

        .. code-block:: python
            :linenos:
            :emphasize-lines: 2

            job_client.stop(
                job_id='Your_job_id_here'
            )

        :param job_id: id of job that we want to stop
        :raises: exceptions.GradientSdkError
        """
        repository = self.build_repository(StopJob)
        repository.stop(job_id)

    def list(self, project_id=None, project=None, experiment_id=None, tags=None):
        """
        Method to list jobs.

        To retrieve all user jobs:

        .. code-block:: python
            :linenos:

            jobs = job_client.list()

        To list jobs from project:

        .. code-block:: python
            :linenos:

            job = job_client.list(
                project_id="Your_project_id_here",
            )

        :param str project_id: id of project that you want to list jobs
        :param str project: name of project that you want to list jobs
        :param str experiment_id: id of experiment that you want to list jobs
        :param list[str]|tuple[str] tags: tags to filter jobs with OR

        :returns: list of job models
        :rtype: list[Job]
        """
        repository = self.build_repository(ListJobs)
        jobs = repository.list(
            project_id=project_id,
            project=project,
            experiment_id=experiment_id,
            tags=tags,
        )
        return jobs

    def logs(self, job_id, line=1, limit=10000):
        """
        Method to retrieve job logs.

        .. code-block:: python
            :linenos:
            :emphasize-lines: 2

            job_logs = job_client.logs(
                job_id='Your_job_id_here',
                line=100,
                limit=100
            )

        :param str job_id: id of job that we want to retrieve logs
        :param int line: from what line you want to retrieve logs. Default 0
        :param int limit: how much lines you want to retrieve logs. Default 10000

        :returns: list of formatted logs lines
        :rtype: list
        """
        repository = self.build_repository(ListJobLogs)
        logs = repository.list(id=job_id, line=line, limit=limit)
        return logs

    def yield_logs(self, job_id, line=1, limit=10000):
        """Get log generator. Polls the API for new logs

        .. code-block:: python
            :linenos:
            :emphasize-lines: 2

            job_logs_generator = job_client.yield_logs(
                job_id='Your_job_id_here',
                line=100,
                limit=100
            )

        :param str job_id:
        :param int line: line number at which logs starts to display on screen
        :param int limit: maximum lines displayed on screen, default set to 10 000

        :returns: generator yielding LogRow instances
        :rtype: Iterator[models.LogRow]
        """

        repository = self.build_repository(ListJobLogs)
        logs = repository.yield_logs(id=job_id, line=line, limit=limit)
        return logs

    def artifacts_delete(self, job_id, files=None):
        """
        Method to delete job artifact.

        .. code-block:: python
            :linenos:
            :emphasize-lines: 2

            job_client.artifacts_delete(
                job_id='Your_job_id_here',
                files=files,
            )

        :param str job_id: Id of job which artifact you want to delete
        :param str files: if you wish to remove only few files from artifact pass string with names of this files
            separated by comma ``,``

        :raises: exceptions.GradientSdkError
        """
        repository = self.build_repository(DeleteJobArtifacts)
        repository.delete(id_=job_id, files=files)

    def artifacts_get(self, job_id):
        """
        Method to retrieve federated access information for job artifacts.

        .. code-block:: python
            :linenos:
            :emphasize-lines: 2

            artifacts = job_client.artifacts_get(
                job_id='your_job_id_here',
            )

        :param job_id: Id of job from which you want to retrieve artifacts information about location

        :returns: Information about artifact place
        :rtype: dict
        """
        repository = self.build_repository(GetJobArtifacts)
        data = repository.get(jobId=job_id)
        return data

    def artifacts_list(self, job_id, files=None, size=False, links=True):
        """
        Method to retrieve all artifacts files.

        .. code-block:: python
            :linenos:
            :emphasize-lines: 2

            artifacts = job_client.artifacts_list(
                job_id='your_job_id_here',
                files='your_files,here',
                size=False,
                links=True
            )

        :param str job_id: to limit artifact from this job.
        :param str files: to limit result only to file names provided. You can use wildcard option ``*``.
        :param bool size: flag to show file size. Default value is set to False.
        :param bool links: flag to show file url. Default value is set to True.

        :returns: list of files with description if specified from job artifacts.
        :rtype: list[Artifact]
        """
        start_after = None
        artifacts = []
        repository = self.build_repository(ListJobArtifacts)

        while True:
            pagination_response = repository.list(jobId=job_id, files=files, links=links, size=size, start_after=start_after)
            artifacts.extend(pagination_response.data)
            start_after = pagination_response.start_after

            if start_after is None:
                break

        return artifacts

    def get_metrics(self, job_id, start=None, end=None, interval="30s", built_in_metrics=None):
        """Get job metrics

        :param str job_id: ID of a job
        :param datetime.datetime|str start:
        :param datetime.datetime|str end:
        :param str interval:
        :param list[str] built_in_metrics: List of metrics to get if different than default
                    Available builtin metrics: cpuPercentage, memoryUsage, gpuMemoryFree, gpuMemoryUsed, gpuPowerDraw,
                                            gpuTemp, gpuUtilization, gpuMemoryUtilization

        :returns: Metrics of a job
        :rtype: dict[str,dict[str,list[dict]]]
        """

        repository = self.build_repository(GetJobMetrics)
        metrics = repository.get(
            id=job_id,
            start=start,
            end=end,
            interval=interval,
            built_in_metrics=built_in_metrics,
        )
        return metrics

    def stream_metrics(self, job_id, interval="30s", built_in_metrics=None):
        """Stream live job metrics

        :param str job_id: ID of a job
        :param str interval:
        :param list[str] built_in_metrics: List of metrics to get if different than default
                    Available builtin metrics: cpuPercentage, memoryUsage, gpuMemoryFree, gpuMemoryUsed, gpuPowerDraw,
                                            gpuTemp, gpuUtilization, gpuMemoryUtilization

        :returns: Generator object yielding live job metrics
        :rtype: Iterable[dict]
        """

        repository = self.build_repository(StreamJobMetrics)
        metrics = repository.stream(
            id=job_id,
            interval=interval,
            built_in_metrics=built_in_metrics,
        )
        return metrics

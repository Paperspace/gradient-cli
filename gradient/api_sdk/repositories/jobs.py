import json

import gradient.api_sdk.config
from .common import ListResources, CreateResource, GetResource, DeleteResource, StopResource, GetMetrics, StreamMetrics, \
    ListLogs
from .. import serializers, sdk_exceptions
from ..clients import http_client
from ..serializers import JobSchema


class GetBaseJobApiUrlMixin(object):
    def _get_api_url(self, **_):
        return gradient.api_sdk.config.config.CONFIG_HOST


class ListJobs(GetBaseJobApiUrlMixin, ListResources):

    def get_request_url(self, **kwargs):
        return "/jobs/getJobList/"

    def _parse_objects(self, data, **kwargs):
        jobs = []

        for job_dict in data["jobList"]:
            job = self._parse_object(job_dict)
            jobs.append(job)

        return jobs

    def _parse_object(self, job_dict):
        job = serializers.JobSchema().get_instance(job_dict)
        return job

    def _get_request_params(self, kwargs):
        filters = {"filter": {"where": {}}}
        if kwargs.get("project_id"):
            filters["filter"]["where"]["projectId"] = kwargs.get("project_id")

        if kwargs.get("project"):
            filters["filter"]["where"]["project"] = kwargs.get("project")

        if kwargs.get("experiment_id"):
            filters["filter"]["where"]["experimentId"] = kwargs.get("experiment_id")

        params = {}
        filter_string = json.dumps(filters)
        params["filter"] = filter_string

        tags = kwargs.get("tags")
        if tags:
            params["modelName"] = "team"  # TODO: filtering by tags won't work without this. Remove this when fixed.
            for i, tag in enumerate(tags):
                key = "tagFilter[{}]".format(i)
                params[key] = tag

        return params or None


class ListJobLogs(ListLogs):
    def _get_request_params(self, kwargs):
        params = {
            "jobId": kwargs["id"],
            "line": kwargs["line"],
            "limit": kwargs["limit"]
        }
        return params


class CreateJob(GetBaseJobApiUrlMixin, CreateResource):
    SERIALIZER_CLS = JobSchema
    HANDLE_FIELD = "id"

    def get_request_url(self, **kwargs):
        return "/jobs/createJob/"

    def _get_id_from_response(self, response):
        handle = response.data[self.HANDLE_FIELD]
        return handle

    def _get_request_json(self, instance_dict):
        return

    def _get_request_params(self, instance_dict):
        return instance_dict


class RunJob(CreateJob):
    def __init__(self, api_key, logger, client):
        super(RunJob, self).__init__(api_key, logger)
        self.http_client = client

    def _get_client(self, **kwargs):
        return self.http_client


class DeleteJob(GetBaseJobApiUrlMixin, DeleteResource):

    def get_request_url(self, **kwargs):
        return "/jobs/{}/destroy".format(kwargs.get("id"))

    def _send_request(self, client, url, json_data=None):
        response = client.post(url, json=json_data)
        return response


class StopJob(GetBaseJobApiUrlMixin, StopResource):

    def get_request_url(self, **kwargs):
        return "/jobs/{}/stop".format(kwargs.get('id'))

    def _send_request(self, client, url, json_data=None):
        response = client.post(url, json=json_data)
        return response


class GetJob(GetBaseJobApiUrlMixin, GetResource):
    def get_request_url(self, **kwargs):
        return "/jobs/getPublicJob"

    def _get_request_json(self, kwargs):
        json_ = {
            "jobId": kwargs["job_id"]
        }
        return json_

    def _send_request(self, client, url, json=None, params=None):
        response = client.post(url, json=json, params=params)
        return response

    def _parse_object(self, instance_dict, **kwargs):
        instance_dict = instance_dict["job"]
        job = serializers.JobSchema().get_instance(instance_dict)
        return job


class ListJobArtifacts(GetBaseJobApiUrlMixin, ListResources):
    def _parse_objects(self, data, **kwargs):
        serializer = serializers.ArtifactSchema()
        files = serializer.get_instance(data, many=True)
        return files

    def get_request_url(self, **kwargs):
        return "/jobs/artifactsList"

    def _get_request_params(self, kwargs):
        params = {
            "jobId": kwargs.get("jobId"),
        }

        if kwargs.get("files"):
            params["files"] = kwargs.get("files")

        if kwargs.get("size"):
            params["size"] = kwargs.get("size")

        if kwargs.get("links"):
            params["links"] = kwargs.get("links")

        return params


class DeleteJobArtifacts(GetBaseJobApiUrlMixin, DeleteResource):
    VALIDATION_ERROR_MESSAGE = "Failed to delete resource"

    def get_request_url(self, **kwargs):
        return "/jobs/{}/artifactsDestroy".format(kwargs.get("id"))

    def _send(self, url, **kwargs):
        client = self._get_client(**kwargs)
        params_data = self._get_request_params(kwargs)
        response = self._send_request(client, url, params_data=params_data)
        gradient_response = http_client.GradientResponse.interpret_response(response)
        return gradient_response

    def _send_request(self, client, url, params_data=None):
        response = client.post(url, params=params_data)
        return response

    def _get_request_params(self, kwargs):
        filters = dict()

        if kwargs.get("files"):
            filters["files"] = kwargs.get("files")

        return filters or None


class GetJobArtifacts(GetBaseJobApiUrlMixin, GetResource):
    def _parse_object(self, data, **kwargs):
        return data

    def _get_request_params(self, kwargs):
        return {
            "jobId": kwargs.get("jobId")
        }

    def get_request_url(self, **kwargs):
        return "/jobs/artifactsGet"


class GetJobMetrics(GetMetrics):
    OBJECT_TYPE = "mljob"

    def _get_instance_by_id(self, instance_id, **kwargs):
        repository = GetJob(self.api_key, logger=self.logger, ps_client_name=self.ps_client_name)
        instance = repository.get(job_id=instance_id)
        return instance

    def _get_start_date(self, instance, kwargs):
        rv = super(GetJobMetrics, self)._get_start_date(instance, kwargs)
        if rv is None:
            raise sdk_exceptions.GradientSdkError("Job has not started yet")

        return rv


class StreamJobMetrics(StreamMetrics):
    OBJECT_TYPE = "mljob"

    def _get_metrics_api_url(self, instance_id, protocol="https"):
        repository = GetJob(api_key=self.api_key, logger=self.logger, ps_client_name=self.ps_client_name)
        instance = repository.get(job_id=instance_id)

        metrics_api_url = super(StreamJobMetrics, self)._get_metrics_api_url(instance, protocol="wss")
        return metrics_api_url

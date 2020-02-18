import json

import gradient.api_sdk.config
from gradient.api_sdk import serializers
from gradient.api_sdk.clients import http_client
from .common import ListResources, CreateResource, GetResource, DeleteResource, StopResource
from ..serializers import JobSchema, LogRowSchema


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


class ListJobLogs(ListResources):
    def _get_api_url(self, **_):
        return gradient.api_sdk.config.config.CONFIG_LOG_HOST

    def get_request_url(self, **kwargs):
        return "/jobs/logs"

    def yield_logs(self, job_id, line=0, limit=10000):
        return self._get_logs_generator(job_id, line, limit)

    def _get_logs_generator(self, job_id, line, limit):
        last_line_number = line

        while True:
            logs = self.list(job_id=job_id, line=line, limit=limit)

            for log in logs:
                if log.message == "PSEOF":
                    return

                last_line_number += 1
                yield log

    def _parse_objects(self, log_rows, **kwargs):
        serializer = LogRowSchema()
        log_rows = (serializer.get_instance(row) for row in log_rows)
        return log_rows

    def _get_request_params(self, kwargs):
        params = {
            "jobId": kwargs["job_id"],
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

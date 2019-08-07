from gradient.api_sdk.clients import http_client
from .common import ListResources, CreateResource, BaseRepository, GetResource
from ..serializers import JobSchema, LogRowSchema


class ParseJobDictMixin(object):
    @staticmethod
    def _parse_object(job_dict, **kwargs):
        """

        :param job_dict:
        :param kwargs:
        :return:
        :rtype: Job
        """
        job = JobSchema().get_instance(job_dict)
        return job


class ListJobs(ParseJobDictMixin, ListResources):

    def get_request_url(self, **kwargs):
        return "/jobs/getJobs/"

    def _parse_objects(self, data, **kwargs):
        jobs = []

        for job_dict in data:
            job = self._parse_object(job_dict)
            jobs.append(job)

        return jobs

    def _get_request_json(self, kwargs):
        filters = kwargs.get("filters")
        json_ = filters or None
        return json_


class ListJobLogs(ListResources):

    def get_request_url(self, **kwargs):
        return "/jobs/logs"

    def yield_logs(self, job_id, line=0, limit=10000):
        pass

    def _get_logs_generator(self, job_id, line, limit):
        last_line_number = line

        while True:
            logs = self.list(job_id=job_id, line=line, limit=limit)

            for log in logs:
                if log.message == "PSEOF":
                    raise StopIteration()

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


class CreateJob(CreateResource):
    SERIALIZER_CLS = JobSchema
    HANDLE_FIELD = "id"

    def _get_create_url(self):
        return "/jobs/createJob/"

    def create_job(self, instance, data):
        instance_dict = self._get_instance_dict(instance)
        url = self._get_create_url()
        response = self.client.post(url, json=instance_dict, data=data)
        gradient_response = http_client.GradientResponse.interpret_response(response)
        self._validate_response(gradient_response)
        handle = self._process_response(response)
        return handle

    def _get_id_from_response(self, response):
        handle = response.json()[self.HANDLE_FIELD]
        return handle


class DeleteJob(BaseRepository):

    def get_request_url(self, **kwargs):
        return "/job/{}/destroy/".format(kwargs.get("id_"))

    def delete(self, id_, **kwargs):
        url = self.get_request_url(id_=id_)
        response = self.client.post(url)
        self._validate_response(response)


class StopJob(BaseRepository):

    def get_request_url(self, **kwargs):
        return "/job/{}/stop/".format(kwargs.get('id_'))

    def stop(self, id_, **kwargs):
        url = self.get_request_url(id_=id_)
        response = self.client.post(url)
        self._validate_response(response)


class ListJobArtifacts(ListResources):
    def _parse_objects(self, data, **kwargs):
        return data

    def get_request_url(self, **kwargs):
        return "/jobs/artifactsList"

    def _get_request_params(self, kwargs):
        return kwargs.get("params")


class DeleteJobArtifacts(BaseRepository):
    VALIDATION_ERROR_MESSAGE = "Failed to delete resource"

    def get_request_url(self, **kwargs):
        return "/jobs/{}/artifactsDestroy/".format(kwargs.get("id_"))

    def delete(self, id_, **kwargs):
        url = self.get_request_url(id_=id_)

        response = self.client.post(url, json=kwargs.get("json"), params=kwargs.get("params"))
        self._validate_response(response)


class GetJobArtifacts(GetResource):
    def _parse_object(self, data, **kwargs):
        return data

    def _get_request_params(self, kwargs):
        return kwargs.get("params")

    def get_request_url(self, **kwargs):
        return "/jobs/artifactsGet"

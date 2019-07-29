from gradient.config import config
from .base_client import BaseClient
from ..clients import http_client
from ..models import Job
from ..serializers import JobSchema
from ..repositories.jobs import ListJobs, ListJobLogs, ListJobArtifacts
from ..utils import MessageExtractor


class JobsClient(BaseClient):
    HOST_URL = config.CONFIG_HOST

    def __init__(self, *args, **kwargs):
        super(JobsClient, self).__init__(*args, **kwargs)
        self.logs_client = http_client.API(config.CONFIG_LOG_HOST,
                                           api_key=self.api_key,
                                           logger=self.logger)

    def create(self, json_, data):
        """
        Method to create job in paperspace cloud.

        :param json_: dict with values for job
        :return: job handle if created with success
        """
        job = Job(**json_)
        job_dict = JobSchema().dump(job).data
        return self._create(job_dict, data)

    def delete(self, job_id):
        url = self._get_action_url(job_id, "destroy")
        response = self.client.post(url)
        return response

    def stop(self, job_id):
        url = self._get_action_url(job_id, "stop")
        response = self.client.post(url)
        return response

    def list(self, filters):
        return ListJobs(self.client).list(filters=filters)

    def logs(self, job_id, line=0, limit=10000):
        logs = ListJobLogs(self.logs_client).list(job_id=job_id, line=line, limit=limit)
        return logs

    def artifacts_delete(self, job_id, params):
        url = self._get_action_url(job_id, "artifactsDestroy", ending_slash=False)
        response = self.client.post(url, params=params)
        return response

    def artifacts_get(self, job_id):
        url = '/jobs/artifactsGet'
        response = self.client.get(url, params={'jobId': job_id})
        return response

    def artifacts_list(self, filters):
        return ListJobArtifacts(self.client).list(filters=filters)

    def _create(self, job_dict, data):
        """

        :param job_dict:
        :param data:
        :return:
        """
        response = self._get_create_response(job_dict, data)
        return response

    def _get_create_response(self, json_, data):
        """

        :param json_:
        :param data:
        :return:
        """
        return self.client.post("/jobs/createJob/", params=json_, data=data)

    @staticmethod
    def _get_error_message(response):
        try:
            response_data = response.json()
        except ValueError:
            return "Unknown error"

        msg = MessageExtractor().get_message_from_response_data(response_data)
        return msg

    @staticmethod
    def _get_action_url(job_id, action, ending_slash=True):
        template_with_ending_slash = "/jobs/{}/{}/"
        template_without_ending_slash = "/jobs/{}/{}"

        if ending_slash:
            template = template_with_ending_slash
        else:
            template = template_without_ending_slash
        return template.format(job_id, action)

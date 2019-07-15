from .base_client import BaseClient
from ..models import Job
from ..serializers import JobSchema
from ..workspace import MultipartEncoder
from ..repositories.jobs import ListJobs
from ..exceptions import GradientSdkError
from ..utils import MessageExtractor


class JobsClient(BaseClient):

    def create(self, json_):
        """
        Method to create job in paperspace cloud.

        :param json_: dict with values for job
        :return: job handle if created with success
        """
        job = Job(**json_)
        job_dict = JobSchema().dump(job).data
        return self._create(job_dict)

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

    def _create(self, job_dict):
        """

        :param job_dict:
        :return:
        """
        json_, data = self._prepare_create_data(job_dict)
        response = self._get_create_response(job_dict, data)
        return response

    def _prepare_create_data(self, job_dict):
        """

        :param job_dict:
        :return:
        """
        data = None

        self._set_project_if_not_provided(job_dict)
        workspace_url = self.workspace_handler.handle(job_dict)
        if workspace_url:
            if self.workspace_handler.archive_path:
                data = self._get_multipart_data(job_dict)
            else:
                job_dict["workspaceFileName"] = workspace_url

        return job_dict, data

    @staticmethod
    def _set_project_if_not_provided(json_):
        if not json_.get("projectId"):
            json_["project"] = "gradient-project"

    def _get_multipart_data(self, json_):
        archive_basename = self.workspace_handler.archive_basename
        json_["workspaceFileName"] = archive_basename
        job_data = self._get_files_dict(archive_basename)
        monitor = MultipartEncoder(job_data).get_monitor()
        self.client.headers["Content-Type"] = monitor.content_type
        data = monitor
        return data

    def _get_files_dict(self, archive_basename):
        job_data = {'file': (archive_basename, open(self.workspace_handler.archive_path, 'rb'), 'text/plain')}
        return job_data

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
    def _get_action_url(job_id, action):
        return "/jobs/{}/{}/".format(job_id, action)

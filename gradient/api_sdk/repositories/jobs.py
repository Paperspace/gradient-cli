from .common import ListResources
from .. import serializers


class ListJobs(ListResources):

    def get_request_url(self, **kwargs):
        return "/jobs/getJobs/"

    def _parse_objects(self, data, **kwargs):
        jobs = []

        for job_dict in data:
            job = serializers.JobSchema().get_instance(job_dict)
            jobs.append(job)

        return jobs

    def _get_request_json(self, kwargs):
        filters = kwargs.get("filters")
        json_ = filters or None
        return json_

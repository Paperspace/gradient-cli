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
        serializer = serializers.LogRowSchema()
        log_rows = (serializer.get_instance(row) for row in log_rows)
        return log_rows

    def _get_request_params(self, kwargs):
        params = {
            'jobId': kwargs['job_id'],
            'line': kwargs['line'],
            'limit': kwargs['limit']
        }
        return params


class ListJobArtifacts(ListResources):
    def _parse_objects(self, data, **kwargs):
        return data

    def get_request_url(self, **kwargs):
        return '/jobs/artifactsList'

    def _get_request_params(self, kwargs):
        return kwargs.get('filters')

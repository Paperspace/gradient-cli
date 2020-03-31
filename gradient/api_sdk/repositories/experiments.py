import abc

import six

from .common import ListResources, GetResource, CreateResource, StartResource, StopResource, DeleteResource
from .. import config, serializers
from ..serializers import utils


class GetBaseExperimentApiUrlMixin(object):
    def _get_api_url(self, **_):
        return config.config.CONFIG_EXPERIMENTS_HOST_V2


class GetBaseExperimentApiUrlBasedOnClusterIdMixin(object):
    def _get_api_url(self, **kwargs):
        if kwargs.get("clusterId"):
            return config.config.CONFIG_EXPERIMENTS_HOST_V2

        return config.config.CONFIG_EXPERIMENTS_HOST


class ParseExperimentDictMixin(object):
    def _parse_object(self, experiment_dict, **kwargs):
        """
        :param dict experiment_dict:
        :rtype BaseExperiment
        """
        serializer = utils.get_serializer_for_experiment(experiment_dict)
        experiment = serializer().get_instance(experiment_dict)
        return experiment


class ListExperiments(ParseExperimentDictMixin, GetBaseExperimentApiUrlMixin, ListResources):
    def get_request_url(self, **kwargs):
        return "/experiments/"

    def _get_meta_data(self, resp):
        return resp.data.get("meta")

    def _parse_objects(self, data, **kwargs):
        experiments_dicts = self._get_experiments_dicts_from_json_data(data, kwargs)
        experiments = []
        for experiment_dict in experiments_dicts:
            experiment_dict.update(experiment_dict["templateHistory"].get("params", {}))
            experiment = self._parse_object(experiment_dict)
            experiments.append(experiment)

        return experiments

    @staticmethod
    def _get_experiments_dicts_from_json_data(data, kwargs):
        filtered = bool(kwargs.get("project_id"))
        if not filtered:  # If filtering by project ID response data has different format...
            return data["data"]

        experiments = []
        for project_experiments in data["data"]:
            for experiment in project_experiments["data"]:
                experiments.append(experiment)

        return experiments

    def _get_request_params(self, kwargs):
        params = {
            "limit": kwargs.get("limit"),
            "offset": kwargs.get("offset")
        }

        project_id = kwargs.get("project_id")
        if project_id:
            if isinstance(project_id, six.string_types):
                project_id = [project_id]
            for i, experiment_id in enumerate(project_id):
                key = "projectHandle[{}]".format(i)
                params[key] = experiment_id

        tags = kwargs.get("tags")
        if tags:
            params["tag"] = tags

        return params


class GetExperiment(ParseExperimentDictMixin, GetBaseExperimentApiUrlMixin, GetResource):
    def _parse_object(self, experiment_dict, **kwargs):
        experiment_dict = experiment_dict["data"]
        experiment_dict.update(experiment_dict["templateHistory"].get("params", {}))
        return super(GetExperiment, self)._parse_object(experiment_dict, **kwargs)

    def get_request_url(self, **kwargs):
        experiment_id = kwargs["experiment_id"]
        url = "/experiments/{}/".format(experiment_id)
        return url


class ListExperimentLogs(ListResources):
    def _get_api_url(self, **kwargs):
        return config.config.CONFIG_LOG_HOST

    def get_request_url(self, **kwargs):
        return "/jobs/logs"

    def list(self, experiment_id, line, limit, **kwargs):
        instances = super(ListExperimentLogs, self).list(experiment_id=experiment_id,
                                                         line=line, limit=limit)
        instances = list(instances)  # because here the _parse_objects returns a generator
        return instances

    def yield_logs(self, experiment_id, line=0, limit=10000):

        gen = self._get_logs_generator(experiment_id, line, limit)
        return gen

    def _get_logs_generator(self, experiment_id, line, limit):
        last_line_number = line

        while True:
            logs = self.list(experiment_id, last_line_number, limit)

            for log in logs:
                # stop generator - "PSEOF" indicates there are no more logs
                if log.message == "PSEOF":
                    return

                last_line_number += 1
                yield log

    def _parse_objects(self, log_rows, **kwargs):
        serializer = serializers.LogRowSchema()
        log_rows = (serializer.get_instance(row) for row in log_rows)
        return log_rows

    def _get_request_params(self, kwargs):
        params = {
            "experimentId": kwargs["experiment_id"],
            "line": kwargs["line"],
            "limit": kwargs["limit"],
        }
        return params


@six.add_metaclass(abc.ABCMeta)
class BaseCreateExperiment(GetBaseExperimentApiUrlBasedOnClusterIdMixin, CreateResource):
    def get_request_url(self, **_):
        return "/experiments/"


class CreateSingleNodeExperiment(BaseCreateExperiment):
    SERIALIZER_CLS = serializers.SingleNodeExperimentSchema


class CreateMultiNodeExperiment(BaseCreateExperiment):
    SERIALIZER_CLS = serializers.MultiNodeExperimentSchema


class CreateMpiMultiNodeExperiment(BaseCreateExperiment):
    SERIALIZER_CLS = serializers.MpiMultiNodeExperimentSchema


class RunSingleNodeExperiment(CreateSingleNodeExperiment):
    def get_request_url(self, **_):
        return "/experiments/run/"


class RunMultiNodeExperiment(CreateMultiNodeExperiment):
    def get_request_url(self, **_):
        return "/experiments/run/"


class RunMpiMultiNodeExperiment(CreateMpiMultiNodeExperiment):
    def get_request_url(self, **_):
        return "/experiments/run/"


class StartExperiment(GetBaseExperimentApiUrlMixin, StartResource):
    VALIDATION_ERROR_MESSAGE = "Failed to start experiment"

    def get_request_url(self, **kwargs):
        id_ = kwargs["id"]
        url = "/experiments/{}/start/".format(id_)
        return url


class StopExperiment(GetBaseExperimentApiUrlMixin, StopResource):
    VALIDATION_ERROR_MESSAGE = "Failed to stop experiment"

    def get_request_url(self, **kwargs):
        id_ = kwargs["id"]
        url = "/experiments/{}/stop/".format(id_)
        return url


class DeleteExperiment(GetBaseExperimentApiUrlMixin, DeleteResource):
    def get_request_url(self, **kwargs):
        experiment_id = kwargs["id"]
        return "/experiments/{}/".format(experiment_id)

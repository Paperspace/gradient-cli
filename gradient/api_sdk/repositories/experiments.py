import abc

import six
import websocket

from .common import ListResources, CreateResource, StartResource, StopResource, DeleteResource, GetResource, GetMetrics, ListMetrics, \
    StreamMetrics, ListLogs
from .. import config, serializers, sdk_exceptions
from ..repositories.jobs import ListJobs
from ..serializers import utils as serializers_utils
from ..utils import concatenate_urls


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
        serializer = serializers_utils.get_serializer_for_experiment(experiment_dict)
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


class ListExperimentLogs(ListLogs):
    def _get_request_params(self, kwargs):
        params = {
            "experimentId": kwargs["id"],
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


class GetExperimentMetricsApiUrlMixin(object):
    def _get_metrics_api_url(self, instance, protocol="https"):
        instance_id = getattr(instance, "id", instance)
        repository = ListJobs(api_key=self.api_key, logger=self.logger, ps_client_name=self.ps_client_name)
        try:
            job = repository.list(experiment_id=instance_id)[0]
        except IndexError:
            raise sdk_exceptions.GradientSdkError("Experiment has not started yet")

        metrics_api_url = concatenate_urls(protocol + "://", job.metrics_url)
        if not job.metrics_url:
            raise sdk_exceptions.GradientSdkError("Metrics API url not found")

        return metrics_api_url


class GetExperimentMetrics(GetExperimentMetricsApiUrlMixin, GetMetrics):
    OBJECT_TYPE = "experiment"

    def _get_instance_by_id(self, instance_id, **kwargs):
        repository = GetExperiment(self.api_key, logger=self.logger, ps_client_name=self.ps_client_name)
        instance = repository.get(experiment_id=instance_id)
        return instance

    def _get_start_date(self, instance, kwargs):
        rv = super(GetExperimentMetrics, self)._get_start_date(instance, kwargs)
        if rv is None:
            raise sdk_exceptions.GradientSdkError("Experiment has not started yet")

        return rv

    def _get_instance(self, response, **kwargs):
        try:
            rv = super(GetExperimentMetrics, self)._get_instance(response, **kwargs)
        except sdk_exceptions.ResourceFetchingError as e:
            if '{"version":' in str(e):
                # TODO: metrics are not working for v1 experiments at the moment
                raise sdk_exceptions.GradientSdkError("Metrics are available for private clusters only")
            else:
                raise

        return rv

class ListExperimentMetrics(GetExperimentMetricsApiUrlMixin, ListMetrics):
    OBJECT_TYPE = "experiment"

    def _get_instance_by_id(self, instance_id, **kwargs):
        repository = GetExperiment(self.api_key, logger=self.logger, ps_client_name=self.ps_client_name)
        instance = repository.get(experiment_id=instance_id)
        return instance

    def _get_start_date(self, instance, kwargs):
        rv = super(ListExperimentMetrics, self)._get_start_date(instance, kwargs)
        if rv is None:
            raise sdk_exceptions.GradientSdkError("Experiment has not started yet")

        return rv

    def _get_instance(self, response, **kwargs):
        try:
            rv = super(ListExperimentMetrics, self)._get_instance(response, **kwargs)
        except sdk_exceptions.ResourceFetchingError as e:
            if '{"version":' in str(e):
                # TODO: metrics are not working for v1 experiments at the moment
                raise sdk_exceptions.GradientSdkError("Custom metrics are available for private clusters only")
            else:
                raise

        return rv

class StreamExperimentMetrics(GetExperimentMetricsApiUrlMixin, StreamMetrics):
    OBJECT_TYPE = "experiment"

    def _get_connection(self, kwargs):
        try:
            ws = super(StreamExperimentMetrics, self)._get_connection(kwargs)
        except websocket.WebSocketBadStatusException as e:
            if "Handshake status 200 OK" in str(e):
                # TODO: metrics are not working for v1 experiments at the moment
                raise sdk_exceptions.GradientSdkError("Metrics are available for private clusters only")
            else:
                raise

        return ws

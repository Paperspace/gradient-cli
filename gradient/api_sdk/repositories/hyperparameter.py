from .common import CreateResource, ListResources, GetResource, StartResource
from .. import serializers
from ..repositories.experiments import ParseExperimentDictMixin, GetBaseExperimentApiUrlMixin


class CreateHyperparameterJob(GetBaseExperimentApiUrlMixin, CreateResource):
    SERIALIZER_CLS = serializers.HyperparameterSchema

    def get_request_url(self, **_):
        return "/hyperopt/"


class CreateAndStartHyperparameterJob(CreateHyperparameterJob):
    def get_request_url(self, **_):
        return "/hyperopt/create_and_start/"


class ListHyperparameterJobs(GetBaseExperimentApiUrlMixin, ParseExperimentDictMixin, ListResources):
    def get_request_url(self, **kwargs):
        return "/hyperopt/"

    def _parse_objects(self, data, **kwargs):
        experiments = []
        for experiment_dict in data["data"]:
            experiment_dict.update(experiment_dict["templateHistory"].get("params", {}))
            experiment = self._parse_object(experiment_dict)
            experiments.append(experiment)

        return experiments

    def _get_request_params(self, kwargs):
        return {"limit": -1}


class GetHyperparameterTuningJob(GetBaseExperimentApiUrlMixin, ParseExperimentDictMixin, GetResource):
    def get_request_url(self, **kwargs):
        id_ = kwargs["id"]
        url = "/hyperopt/{}/".format(id_)
        return url

    def _parse_object(self, job_dict, **kwargs):
        data = job_dict["data"]
        data.update(data["templateHistory"].get("params", {}))
        instance = super(GetHyperparameterTuningJob, self)._parse_object(data)
        return instance


class StartHyperparameterTuningJob(GetBaseExperimentApiUrlMixin, StartResource):
    VALIDATION_ERROR_MESSAGE = "Failed to start hyperparameter tuning job"

    def get_request_url(self, **kwargs):
        id_ = kwargs["id"]
        url = "/hyperopt/{}/start/".format(id_)
        return url

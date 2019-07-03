from .common import ListResources
from .. import serializers


class ListExperiments(ListResources):
    @property
    def request_url(self):
        return "/experiments/"

    def _parse_objects(self, data, **kwargs):
        experiments_dicts = self._get_experiments_dicts_from_json_data(data, kwargs)
        experiments = []
        for experiment_dict in experiments_dicts:
            experiment_dict.update(experiment_dict["templateHistory"]["params"])

            if self._is_single_node_experiment(experiment_dict):
                experiment = serializers.SingleNodeExperimentSchema().get_instance(experiment_dict)
            else:
                experiment = serializers.MultiNodeExperimentSchema().get_instance(experiment_dict)
            experiments.append(experiment)

        return experiments

    @staticmethod
    def _is_single_node_experiment(experiment_dict):
        return "parameter_server_machine_type" not in experiment_dict["templateHistory"]["params"]

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
        params = {"limit": -1}  # so the API sends back full list without pagination

        project_id = kwargs.get("project_id")
        if project_id:
            for i, experiment_id in enumerate(project_id):
                key = "projectHandle[{}]".format(i)
                params[key] = experiment_id

        return params

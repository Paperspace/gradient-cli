from gradient.commands import common


class ListModelsCommand(common.ListCommand):
    @property
    def request_url(self):
        return "/mlModels/getModelList/"

    def _get_request_params(self, kwargs):
        params = {"limit": -1}  # so the api returns full list without pagination
        return params

    def _get_request_json(self, kwargs):
        filters = kwargs.get("filters")
        if not filters:
            return None

        json_ = {"filter": {"where": {"and": [filters]}}}
        return json_

    def _get_objects(self, response, kwargs):
        data = response.json()["modelList"]
        return data

    def _get_table_data(self, models):
        data = [("Name", "ID", "Model Type", "Project ID", "Experiment ID")]
        for model in models:
            name = model.get("name")
            id_ = model.get("id")
            model_type = model.get("modelType")
            project_id = model.get("projectId")
            experiment_id = model.get("experimentId")
            data.append((name, id_, model_type, project_id, experiment_id))

        return data

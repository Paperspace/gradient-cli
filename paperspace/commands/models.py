import pydoc

import terminaltables

from paperspace.utils import get_terminal_lines

from paperspace.commands import CommandBase


class ListModelsCommand(CommandBase):
    def execute(self, filters):
        json_ = self._get_request_json(filters)
        params = {"limit": -1}  # so the api returns full list without pagination
        response = self.api.get("/mlModels/getModelList/", json=json_, params=params)

        try:
            models = self._get_models_list(response)
        except (ValueError, KeyError) as e:
            self.logger.log("Error while parsing response data: {}".format(e))
        else:
            self._log_models_list(models)

    @staticmethod
    def _get_request_json(filters):
        experiment_id = filters.get("experimentId")
        if not experiment_id:
            return None

        json_ = {"filter": {"where": {"and": [{"experimentId": experiment_id}]}}}
        return json_

    def _get_models_list(self, response):
        if not response.ok:
            raise ValueError("Unknown error")

        data = response.json()["modelList"]
        self.logger.debug(data)
        return data

    def _log_models_list(self, model):
        if not model:
            self.logger.log("No models found")
        else:
            table_str = self._make_models_list_table(model)
            if len(table_str.splitlines()) > get_terminal_lines():
                pydoc.pager(table_str)
            else:
                self.logger.log(table_str)

    @staticmethod
    def _make_models_list_table(models):
        data = [("Name", "ID", "Model Type", "Project ID", "Experiment ID")]
        for model in models:
            name = model.get("name")
            id_ = model.get("id")
            model_type = model.get("modelType")
            project_id = model.get("projectId")
            experiment_id = model.get("experimentId")
            data.append((name, id_, model_type, project_id, experiment_id))

        ascii_table = terminaltables.AsciiTable(data)
        table_string = ascii_table.table
        return table_string


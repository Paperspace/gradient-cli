import pydoc

import terminaltables

from paperspace.commands import CommandBase
from paperspace.utils import get_terminal_lines


class ListModelsCommand(CommandBase):
    def execute(self, filters):
        json_ = self._get_request_json(filters)
        params = {"limit": -1}  # so the api returns full list without pagination
        response = self.api.get("/mlModels/getModelList/", json=json_, params=params)

        try:
            data = response.json()
            if not response.ok:
                self.logger.log_error_response(data)
                return
            models = self._get_objects_list(response)
        except (ValueError, KeyError) as e:
            self.logger.error("Error while parsing response data: {}".format(e))
        else:
            self._log_models_list(models)

    @staticmethod
    def _get_request_json(filters):
        if not filters:
            return None

        json_ = {"filter": {"where": {"and": [filters]}}}
        return json_

    @staticmethod
    def _get_objects_list(response):
        data = response.json()["modelList"]
        return data

    def _log_models_list(self, models):
        if not models:
            self.logger.warning("No models found")
        else:
            table_str = self._make_models_list_table(models)
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

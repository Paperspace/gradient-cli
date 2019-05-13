from paperspace.commands import common


class HyperparametersCommandBase(common.CommandBase):
    def _log_message(self, response, success_msg_template, error_msg):
        if response.ok:
            try:
                json_ = response.json()
            except (ValueError, KeyError):
                self.logger.log(success_msg_template)
            else:
                msg = success_msg_template.format(**json_)
                self.logger.log(msg)
        else:
            try:
                data = response.json()
                self.logger.log_error_response(data)
            except ValueError:
                self.logger.error(error_msg)


class CreateHyperparameterCommand(HyperparametersCommandBase):
    def execute(self, hyperparameter):
        response = self.api.post("/hyperopt/", json=hyperparameter)
        self._log_message(response,
                          "Hyperparameter created with ID: {handle}",
                          "Unknown error while creating hyperparameter")


class ListHyperparametersCommand(common.ListCommand):
    @property
    def request_url(self):
        return "/hyperopt/"

    def _get_table_data(self, objects):
        data = [("Name", "ID", "Project ID")]
        for obj in objects:
            name = obj["templateHistory"]["params"].get("name")
            id_ = obj.get("handle")
            project_id = obj["templateHistory"]["params"].get("project_handle")
            data.append((name, id_, project_id))

        return data

    def _get_objects(self, response, kwargs):
        objects = super(ListHyperparametersCommand, self)._get_objects(response, kwargs)["data"]
        return objects

    def _get_request_params(self, kwargs):
        params = {"limit": -1}
        return params

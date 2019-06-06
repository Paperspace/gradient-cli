import terminaltables

from gradient.commands import common


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


class CreateAndStartHyperparameterCommand(HyperparametersCommandBase):
    def execute(self, hyperparameter):
        response = self.api.post("/hyperopt/create_and_start/", json=hyperparameter)
        self._log_message(response,
                          "Hyperparameter created with ID: {handle} and started",
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


class DeleteHyperparameterCommand(HyperparametersCommandBase):
    def execute(self, id_):
        url = "/hyperopt/{}/".format(id_)
        response = self.api.delete(url)
        self._log_message(response,
                          "Hyperparameter deleted",
                          "Unknown error while deleting hyperparameter")


class HyperparameterDetailsCommand(HyperparametersCommandBase):
    def execute(self, id_):
        url = "/hyperopt/{}/".format(id_)
        response = self.api.get(url)

        try:
            data = response.json()
            if not response.ok:
                self.logger.log_error_response(data)
                return

            table = self.make_details_table(data)
        except (ValueError, KeyError) as e:
            self.logger.error("Error while parsing response data: {}".format(e))
        else:
            self.logger.log(table)

    @staticmethod
    def make_details_table(obj):
        data = (
            ("ID", obj["data"].get("handle")),
            ("Name", obj["data"]["templateHistory"]["params"].get("name")),
            ("Ports", obj["data"]["templateHistory"]["params"].get("ports")),
            ("Project ID", obj["data"]["templateHistory"]["params"].get("project_handle")),
            ("Tuning command", obj["data"]["templateHistory"]["params"].get("tuning_command")),
            ("Worker command", obj["data"]["templateHistory"]["params"].get("worker_command")),
            ("Worker container", obj["data"]["templateHistory"]["params"].get("worker_container")),
            ("Worker count", obj["data"]["templateHistory"]["params"].get("worker_count")),
            ("Worker machine type", obj["data"]["templateHistory"]["params"].get("worker_machine_type")),
            ("Worker use dockerfile", obj["data"]["templateHistory"]["params"].get("worker_use_dockerfile")),
            ("Workspace URL", obj["data"]["templateHistory"]["params"].get("workspaceUrl")),
        )
        ascii_table = terminaltables.AsciiTable(data)
        table_string = ascii_table.table
        return table_string


class HyperparameterStartCommand(HyperparametersCommandBase):
    def execute(self, id_):
        url = "/hyperopt/{}/start/".format(id_)
        response = self.api.put(url)
        self._log_message(response,
                          "Hyperparameter tuning started",
                          "Unknown error while starting hyperparameter tuning")

from gradient import config, version, client
from gradient.commands import common

default_headers = {"X-API-Key": config.PAPERSPACE_API_KEY,
                   "ps_client_name": "paperspace-python",
                   "ps_client_version": version.version}
deployments_api = client.API(config.CONFIG_HOST, headers=default_headers)


class _DeploymentCommandBase(common.CommandBase):
    def _log_message(self, response, success_msg_template, error_msg):
        if response.ok:
            try:
                j = response.json()
                handle = j["deployment"]
            except (ValueError, KeyError):
                self.logger.error(success_msg_template)
            else:
                msg = success_msg_template.format(**handle)
                self.logger.log(msg)
        else:
            try:
                data = response.json()
                self.logger.log_error_response(data)
            except ValueError:
                self.logger.error(error_msg)


class CreateDeploymentCommand(_DeploymentCommandBase):
    def execute(self, kwargs):
        response = self.api.post("/deployments/createDeployment/", json=kwargs)
        self._log_message(response,
                          "New deployment created with id: {id}",
                          "Unknown error during deployment")


class ListDeploymentsCommand(common.ListCommand):
    @property
    def request_url(self):
        return "/deployments/getDeploymentList/"

    def _get_request_json(self, kwargs):
        filters = kwargs.get("filters")
        if not filters:
            return None

        json_ = {"filter": {"where": {"and": [filters]}}}
        return json_

    def _get_objects(self, response, kwargs):
        data = super(ListDeploymentsCommand, self)._get_objects(response, kwargs)
        objects = data["deploymentList"]
        return objects

    def _get_table_data(self, deployments):
        data = [("Name", "ID", "Endpoint", "Api Type", "Deployment Type")]
        for deployment in deployments:
            name = deployment.get("name")
            id_ = deployment.get("id")
            endpoint = deployment.get("endpoint")
            api_type = deployment.get("apiType")
            deployment_type = deployment.get("deploymentType")
            data.append((name, id_, endpoint, api_type, deployment_type))

        return data


class StartDeploymentCommand(_DeploymentCommandBase):
    def execute(self, deployment_id):
        json_ = {"id": deployment_id,
                 "isRunning": True}
        response = self.api.post("/deployments/updateDeployment/", json=json_)
        self._log_message(response,
                          "Deployment started",
                          "Unknown error occurred.")

class StopDeploymentCommand(_DeploymentCommandBase):
    def execute(self, deployment_id):
        json_ = {"id": deployment_id,
                 "isRunning": False}
        response = self.api.post("/deployments/updateDeployment/", json=json_)
        self._log_message(response,
                          "Deployment stopped",
                          "Unknown error occurred.")

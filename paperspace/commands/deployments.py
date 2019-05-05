import pydoc

import terminaltables

from paperspace import config, version, client, logger
from paperspace.commands import CommandBase
from paperspace.utils import get_terminal_lines

default_headers = {"X-API-Key": config.PAPERSPACE_API_KEY,
                   "ps_client_name": "paperspace-python",
                   "ps_client_version": version.version}
deployments_api = client.API(config.CONFIG_HOST, headers=default_headers)


class _DeploymentCommandBase(CommandBase):
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


class ListDeploymentsCommand(_DeploymentCommandBase):
    def execute(self, filters=None):
        json_ = self._get_request_json(filters)
        response = self.api.get("/deployments/getDeploymentList/", json=json_)

        try:
            data = response.json()
            if not response.ok:
                self.logger.log_error_response(data)
                return
            deployments = self._get_deployments_list(response)
        except (ValueError, KeyError) as e:
            self.logger.error("Error while parsing response data: {}".format(e))
        else:
            self._log_deployments_list(deployments)

    @staticmethod
    def _get_request_json(filters):
        if not filters:
            return None

        json_ = {"filter": {"where": {"and": [filters]}}}
        return json_

    @staticmethod
    def _get_deployments_list(response):
        if not response.ok:
            raise ValueError("Unknown error")

        data = response.json()["deploymentList"]
        logger.debug(data)
        return data

    def _log_deployments_list(self, deployments):
        if not deployments:
            self.logger.warning("No deployments found")
        else:
            table_str = self._make_deployments_list_table(deployments)
            if len(table_str.splitlines()) > get_terminal_lines():
                pydoc.pager(table_str)
            else:
                self.logger.log(table_str)

    @staticmethod
    def _make_deployments_list_table(deployments):
        data = [("Name", "ID", "Endpoint", "Api Type", "Deployment Type")]
        for deployment in deployments:
            name = deployment.get("name")
            id_ = deployment.get("id")
            endpoint = deployment.get("endpoint")
            api_type = deployment.get("apiType")
            deployment_type = deployment.get("deploymentType")
            data.append((name, id_, endpoint, api_type, deployment_type))

        ascii_table = terminaltables.AsciiTable(data)
        table_string = ascii_table.table
        return table_string


class UpdateDeploymentCommand(_DeploymentCommandBase):
    def execute(self, deployment_id, kwargs):
        if not kwargs:
            self.logger.log("No parameters to update were given. Use --help for more information.")
            return

        json_ = {"id": deployment_id,
                 "upd": kwargs}
        response = self.api.post("/deployments/updateDeployment/", json=json_)
        self._log_message(response,
                          "Deployment model updated.",
                          "Unknown error occurred.")


class StartDeploymentCommand(_DeploymentCommandBase):
    def execute(self, deployment_id):
        json_ = {"id": deployment_id,
                 "isRunning": True}
        response = self.api.post("/deployments/updateDeployment/", json=json_)
        self._log_message(response,
                          "Deployment started",
                          "Unknown error occurred.")


class DeleteDeploymentCommand(_DeploymentCommandBase):
    def execute(self, deployment_id):
        json_ = {"id": deployment_id,
                 "upd": {"isDeleted": True}}
        response = self.api.post("/deployments/updateDeployment/", json=json_)
        self._log_message(response,
                          "Deployment deleted.",
                          "Unknown error occurred.")

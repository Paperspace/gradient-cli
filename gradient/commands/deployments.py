import abc
import json
import pydoc

import six
import terminaltables
from click import style
from halo import halo

from gradient import exceptions, DeploymentsClient
from gradient.api_sdk import sdk_exceptions, utils, models
from gradient.api_sdk.config import config
from gradient.api_sdk.utils import concatenate_urls
from gradient.cli_constants import CLI_PS_CLIENT_NAME
from gradient.cliutils import get_terminal_lines
from gradient.commands.common import DetailsCommandMixin, StreamMetricsCommand, BaseCommand, LogsCommandMixin


@six.add_metaclass(abc.ABCMeta)
class BaseDeploymentCommand(BaseCommand):
    def _get_client(self, api_key, logger):
        client = DeploymentsClient(
            api_key=api_key,
            logger=logger,
            ps_client_name=CLI_PS_CLIENT_NAME,
        )
        return client


class HandleWorkspaceMixin(object):
    def _handle_workspace(self, instance_dict):
        handler = self.workspace_handler.handle(instance_dict)

        instance_dict.pop("ignore_files", None)
        instance_dict.pop("workspace", None)
        if handler and handler != "none":
            instance_dict["workspace_url"] = handler


class CreateDeploymentCommand(BaseDeploymentCommand, HandleWorkspaceMixin):
    def __init__(self, workspace_handler, *args, **kwargs):
        super(CreateDeploymentCommand, self).__init__(*args, **kwargs)
        self.workspace_handler = workspace_handler

    def execute(self, **kwargs):
        self._handle_auth(kwargs)
        self._handle_workspace(kwargs)
        with halo.Halo(text="Creating new deployment", spinner="dots"):
            deployment_id = self.client.create(**kwargs)

        self.logger.log("New deployment created with id: {}".format(deployment_id))
        self.logger.log(self.get_instance_url(deployment_id))

    def get_instance_url(self, instance_id):
        url = concatenate_urls(config.WEB_URL, "/console/deployments/{}".format(instance_id))
        return url

    def _handle_auth(self, kwargs):
        if kwargs.pop("generate_auth", False):
            auth_username, auth_password = utils.generate_credentials_pair(12)
            kwargs["auth_username"] = auth_username
            kwargs["auth_password"] = auth_password
            self.logger.log("Generated credentials: \nusername:{}\npassword:{}".format(auth_password, auth_username))


class ListDeploymentsCommand(BaseDeploymentCommand):
    WAITING_FOR_RESPONSE_MESSAGE = "Waiting for data..."

    def execute(self, **kwargs):
        with halo.Halo(text=self.WAITING_FOR_RESPONSE_MESSAGE, spinner="dots"):
            instances = self._get_instances(**kwargs)

        self._log_objects_list(instances)

    def _get_instances(self, **kwargs):
        try:
            instances = self.client.list(**kwargs)
        except sdk_exceptions.GradientSdkError as e:
            raise exceptions.ReceivingDataFailedError(e)

        return instances

    @staticmethod
    def _get_table_data(deployments):
        data = [("Name", "ID", "Endpoint", "Api Type", "Deployment Type", "Deployment State")]
        for deployment in deployments:
            name = deployment.name
            id_ = deployment.id
            endpoint = deployment.endpoint
            api_type = deployment.api_type
            deployment_type = deployment.deployment_type
            deployment_state = deployment.state
            data.append((name, id_, endpoint, api_type, deployment_type, deployment_state))

        return data

    def _log_objects_list(self, objects):
        if not objects:
            self.logger.warning("No data found")
            return

        table_data = self._get_table_data(objects)
        table_str = self._make_table(table_data)
        if len(table_str.splitlines()) > get_terminal_lines():
            pydoc.pager(table_str)
        else:
            self.logger.log(table_str)

    @staticmethod
    def _make_table(table_data):
        ascii_table = terminaltables.AsciiTable(table_data)
        table_string = ascii_table.table
        return table_string


class StartDeploymentCommand(BaseDeploymentCommand):
    def execute(self, **kwargs):
        self.client.start(**kwargs)
        self.logger.log("Deployment started")


class StopDeploymentCommand(BaseDeploymentCommand):
    def execute(self, **kwargs):
        self.client.stop(**kwargs)
        self.logger.log("Deployment stopped")


class DeleteDeploymentCommand(BaseDeploymentCommand):
    def execute(self, **kwargs):
        self.client.delete(**kwargs)
        self.logger.log("Deployment deleted")


class UpdateDeploymentCommand(BaseDeploymentCommand, HandleWorkspaceMixin):
    def __init__(self, workspace_handler, *args, **kwargs):
        super(UpdateDeploymentCommand, self).__init__(*args, **kwargs)
        self.workspace_handler = workspace_handler

    def execute(self, deployment_id, **kwargs):
        self._handle_workspace(kwargs)

        with halo.Halo(text="Updating deployment data", spinner="dots"):
            self.client.update(deployment_id, **kwargs)

        self.logger.log("Deployment data updated")


class GetDeploymentDetails(DetailsCommandMixin, BaseDeploymentCommand):
    def _get_table_data(self, instance):
        """
        :param models.Deployment instance:
        """
        tags_string = ", ".join(instance.tags)

        data = (
            ("ID", instance.id),
            ("Name", instance.name),
            ("State", instance.state),
            ("Machine type", instance.machine_type),
            ("Instance count", instance.instance_count),
            ("Command", instance.command),
            ("Deployment type", instance.deployment_type),
            ("Model ID", instance.model_id),
            ("Project ID", instance.project_id),
            ("Endpoint", instance.endpoint),
            ("API type", instance.api_type),
            ("Cluster ID", instance.cluster_id),
            ("Tags", tags_string),
        )
        return data


class DeploymentAddTagsCommand(BaseDeploymentCommand):
    def execute(self, deployment_id, *args, **kwargs):
        self.client.add_tags(deployment_id, **kwargs)
        self.logger.log("Tags added to deployment")


class DeploymentRemoveTagsCommand(BaseDeploymentCommand):
    def execute(self, deployment_id, *args, **kwargs):
        self.client.remove_tags(deployment_id, **kwargs)
        self.logger.log("Tags removed from deployment")


class GetDeploymentMetricsCommand(BaseDeploymentCommand):
    def execute(self, deployment_id, start, end, interval, built_in_metrics, *args, **kwargs):
        metrics = self.client.get_metrics(
            deployment_id,
            start=start,
            end=end,
            built_in_metrics=built_in_metrics,
            interval=interval,
        )
        formatted_metrics = json.dumps(metrics, indent=2, sort_keys=True)
        self.logger.log(formatted_metrics)


class StreamDeploymentMetricsCommand(StreamMetricsCommand, BaseDeploymentCommand):
    pass


class DeploymentLogsCommand(LogsCommandMixin, BaseDeploymentCommand):
    def _make_table(self, logs, experiment_id):
        table_title = "Deployment %s logs" % experiment_id
        table_data = [("LINE", "MESSAGE")]
        table = terminaltables.AsciiTable(table_data, title=table_title)

        for log in logs:
            table_data.append(self._format_row(experiment_id, log))

        return table.table

    def _get_log_row_string(self, id, log):
        log_msg = "{}\t{}".format(*self._format_row(id, log))
        return log_msg

    @staticmethod
    def _format_row(id, log_row):
        return (style(fg="red", text=str(log_row.line)),
                log_row.message)

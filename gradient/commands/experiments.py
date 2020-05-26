import abc
import json

import click
import six
import terminaltables
from click import style
from halo import halo

from gradient import api_sdk, exceptions, TensorboardClient
from gradient.api_sdk import constants, sdk_exceptions
from gradient.api_sdk.config import config
from gradient.api_sdk.utils import concatenate_urls
from gradient.cli_constants import CLI_PS_CLIENT_NAME
from gradient.clilogger import CliLogger
from gradient.cliutils import none_strings_to_none_objects
from gradient.commands import tensorboards as tensorboards_commands
from gradient.commands.common import BaseCommand, ListCommandMixin, DetailsCommandMixin, StreamMetricsCommand, \
    LogsCommandMixin

try:
    # Python 3
    from itertools import zip_longest
except ImportError:
    # Python 2
    from itertools import izip_longest as zip_longest


@six.add_metaclass(abc.ABCMeta)
class BaseExperimentCommand(BaseCommand):
    entity = "experiment"

    def _get_client(self, api_key, logger):
        client = api_sdk.clients.ExperimentsClient(
            api_key=api_key,
            logger=logger,
            ps_client_name=CLI_PS_CLIENT_NAME,
        )
        return client


class TensorboardHandler(object):
    def __init__(self, api_key, logger=CliLogger()):
        self.api_key = api_key
        self.logger = logger

    def maybe_add_to_tensorboard(self, tensorboard_id, experiment_id):
        """Add experiment to existing or new tensorboard

        :param str|bool tensorboard_id:
        :param str experiment_id:
        """
        if isinstance(tensorboard_id, six.string_types):
            self._add_experiment_to_tensorboard(tensorboard_id, experiment_id)
            return

        tensorboards = self._get_tensorboards()
        if len(tensorboards) == 1:
            self._add_experiment_to_tensorboard(tensorboards[0].id, experiment_id)
        else:
            self._create_tensorboard_with_experiment(experiment_id)

    def _add_experiment_to_tensorboard(self, tensorboard_id, experiment_id):
        """Add experiment to tensorboard

        :param str tensorboard_id:
        :param str experiment_id:
        """
        command = tensorboards_commands.AddExperimentToTensorboard(api_key=self.api_key)
        command.execute(tensorboard_id, [experiment_id])

    def _get_tensorboards(self):
        """Get tensorboards

        :rtype: list[api_sdk.Tensorboard]
        """
        tensorboard_client = TensorboardClient(api_key=self.api_key, logger=self.logger)
        tensorboards = tensorboard_client.list()
        return tensorboards

    def _create_tensorboard_with_experiment(self, experiment_id):
        """Create tensorboard with experiment

        :param str experiment_id:
        """
        command = tensorboards_commands.CreateTensorboardCommand(api_key=self.api_key)
        command.execute(experiments=[experiment_id])


@six.add_metaclass(abc.ABCMeta)
class BaseCreateExperimentCommandMixin(object):
    SPINNER_MESSAGE = "Creating new experiment"
    CREATE_SUCCESS_MESSAGE_TEMPLATE = "New experiment created with ID: {}"

    def __init__(self, workspace_handler, *args, **kwargs):
        super(BaseCreateExperimentCommandMixin, self).__init__(*args, **kwargs)
        self.workspace_handler = workspace_handler

    def execute(self, json_, add_to_tensorboard=False):
        self._handle_workspace(json_)
        self._handle_dataset_data(json_)

        with halo.Halo(text=self.SPINNER_MESSAGE, spinner="dots"):
            experiment_id = self._create(json_)

        self.logger.log(self.CREATE_SUCCESS_MESSAGE_TEMPLATE.format(experiment_id))
        self.logger.log(self.get_instance_url(experiment_id, json_["project_id"]))

        self._maybe_add_to_tensorboard(add_to_tensorboard, experiment_id, self.api_key)
        return experiment_id

    def get_instance_url(self, instance_id, project_id):
        url = concatenate_urls(config.WEB_URL, "console/projects/{}/experiments/{}".format(project_id, instance_id))
        return url

    def _handle_workspace(self, instance_dict):
        handler = self.workspace_handler.handle(instance_dict)

        instance_dict.pop("ignore_files", None)
        instance_dict.pop("workspace", None)
        instance_dict.pop("workspace_archive", None)
        instance_dict.pop("workspace_url", None)
        if handler and handler != "none":
            instance_dict["workspace_url"] = handler

    def _maybe_add_to_tensorboard(self, tensorboard_id, experiment_id, api_key):
        """
        :param str|bool tensorboard_id:
        :param str experiment_id:
        :param str api_key:
        """
        if tensorboard_id is not False:
            tensorboard_handler = TensorboardHandler(api_key)
            tensorboard_handler.maybe_add_to_tensorboard(tensorboard_id, experiment_id)

    @staticmethod
    def _handle_dataset_data(json_):
        """Make list of dataset dicts"""
        datasets = [
            json_.pop("dataset_uri_list", ()),
            json_.pop("dataset_name_list", ()),
            json_.pop("dataset_access_key_id_list", ()),
            json_.pop("dataset_secret_access_key_list", ()),
            json_.pop("dataset_version_id_list", ()),
            json_.pop("dataset_etag_list", ()),
            json_.pop("dataset_volume_kind_list", ()),
            json_.pop("dataset_volume_size_list", ()),
        ]

        if not any(datasets):
            return
        else:
            dataset_uri_len = len(datasets[0])
            other_dataset_param_max_len = max(len(elem) for elem in datasets[1:])
            if dataset_uri_len < other_dataset_param_max_len:
                # there no point in defining n+1 dataset parameters of one type for n datasets
                raise click.BadParameter(
                    "Too many dataset parameter sets ({}) for {} dataset URIs. Forgot to add one more dataset URI?"
                        .format(other_dataset_param_max_len, dataset_uri_len))

        datasets = [none_strings_to_none_objects(d) for d in datasets]

        datasets = zip_longest(*datasets, fillvalue=None)
        datasets = [{"uri": dataset[0],
                     "name": dataset[1],
                     "aws_access_key_id": dataset[2],
                     "aws_secret_access_key": dataset[3],
                     "version_id": dataset[4],
                     "etag": dataset[5],
                     "volume_kind": dataset[6],
                     "volume_size": dataset[7],
                     } for dataset in datasets]

        json_["datasets"] = datasets

    @abc.abstractmethod
    def _create(self, json_):
        pass


class CreateSingleNodeExperimentCommand(BaseCreateExperimentCommandMixin, BaseExperimentCommand):
    def _create(self, json_):
        handle = self.client.create_single_node(**json_)
        return handle


class CreateMultiNodeExperimentCommand(BaseCreateExperimentCommandMixin, BaseExperimentCommand):
    def _create(self, json_):
        handle = self.client.create_multi_node(**json_)
        return handle


class CreateMpiMultiNodeExperimentCommand(BaseCreateExperimentCommandMixin, BaseExperimentCommand):
    def _create(self, json_):
        json_.pop("experiment_type_id", None)  # for MPI there is no experiment_type_id parameter in client method
        handle = self.client.create_mpi_multi_node(**json_)
        return handle


class CreateAndStartMultiNodeExperimentCommand(BaseCreateExperimentCommandMixin, BaseExperimentCommand):
    SPINNER_MESSAGE = "Creating and starting new experiment"
    CREATE_SUCCESS_MESSAGE_TEMPLATE = "New experiment created and started with ID: {}"

    def _create(self, json_):
        handle = self.client.run_multi_node(**json_)
        return handle


class CreateAndStartMpiMultiNodeExperimentCommand(BaseCreateExperimentCommandMixin, BaseExperimentCommand):
    SPINNER_MESSAGE = "Creating and starting new experiment"
    CREATE_SUCCESS_MESSAGE_TEMPLATE = "New experiment created and started with ID: {}"

    def _create(self, json_):
        json_.pop("experiment_type_id", None)  # for MPI there is no experiment_type_id parameter in client method
        handle = self.client.run_mpi_multi_node(**json_)
        return handle


class CreateAndStartSingleNodeExperimentCommand(BaseCreateExperimentCommandMixin, BaseExperimentCommand):
    SPINNER_MESSAGE = "Creating and starting new experiment"
    CREATE_SUCCESS_MESSAGE_TEMPLATE = "New experiment created and started with ID: {}"

    def _create(self, json_):
        handle = self.client.run_single_node(**json_)
        return handle


class StartExperimentCommand(BaseExperimentCommand):
    def execute(self, experiment_id):
        """
        :param str experiment_id:
        """
        self.client.start(experiment_id)
        self.logger.log("Experiment started")


class StopExperimentCommand(BaseExperimentCommand):
    def execute(self, experiment_id):
        """
        :param str experiment_id:
        """
        self.client.stop(experiment_id)
        self.logger.log("Experiment stopped")


class ListExperimentsCommand(ListCommandMixin, BaseExperimentCommand):
    TOTAL_ITEMS_KEY = "totalItems"

    def _get_instances(self, **kwargs):
        try:
            instances, meta_data = self.client.list(get_meta=True, **kwargs)
        except sdk_exceptions.GradientSdkError as e:
            raise exceptions.ReceivingDataFailedError(e)

        return instances, meta_data

    def _get_table_data(self, experiments):
        data = [("Name", "ID", "Status")]
        for experiment in experiments:
            name = experiment.name
            handle = experiment.id
            status = constants.ExperimentState.get_state_str(experiment.state)
            data.append((name, handle, status))
        return data

    def execute(self, **kwargs):
        return self._generate_data_table(**kwargs)


class GetExperimentCommand(DetailsCommandMixin, BaseExperimentCommand):
    def _get_table_data(self, experiment):
        """
        :param api_sdk.SingleNodeExperiment|api_sdk.MultiNodeExperiment|api_sdk.MpiMultiNodeExperiment experiment:
        """
        if experiment.experiment_type_id == constants.ExperimentType.SINGLE_NODE:
            return self._get_single_node_data(experiment)

        if experiment.experiment_type_id == constants.ExperimentType.GRPC_MULTI_NODE:
            return self._get_multi_node_grpc_data(experiment)

        if experiment.experiment_type_id == constants.ExperimentType.MPI_MULTI_NODE:
            return self._get_multi_node_mpi_data(experiment)

        raise ValueError("Wrong experiment type: {}".format(experiment.experiment_type_id))

    @staticmethod
    def _get_single_node_data(experiment):
        """
        :param api_sdk.SingleNodeExperiment experiment:
        """

        tags_string = ", ".join(experiment.tags)
        data = (
            ("Name", experiment.name),
            ("ID", experiment.id),
            ("State", constants.ExperimentState.get_state_str(experiment.state)),
            ("Ports", experiment.ports),
            ("Project ID", experiment.project_id),
            ("Worker Command", experiment.command),
            ("Worker Container", experiment.container),
            ("Worker Machine Type", experiment.machine_type),
            ("Working Directory", experiment.working_directory),
            ("Workspace URL", experiment.workspace_url),
            ("Model Type", experiment.model_type),
            ("Model Path", experiment.model_path),
            ("Tags", tags_string),
        )
        return data

    @staticmethod
    def _get_multi_node_grpc_data(experiment):
        """
        :param api_sdk.MultiNodeExperiment experiment:
        """

        tags_string = ", ".join(experiment.tags)
        data = (
            ("Name", experiment.name),
            ("ID", experiment.id),
            ("State", constants.ExperimentState.get_state_str(experiment.state)),
            ("Artifact directory", experiment.artifact_directory),
            ("Cluster ID", experiment.cluster_id),
            ("Experiment Env", experiment.experiment_env),
            ("Experiment Type", constants.ExperimentType.get_type_str(experiment.experiment_type_id)),
            ("Model Type", experiment.model_type),
            ("Model Path", experiment.model_path),
            ("Parameter Server Command", experiment.parameter_server_command),
            ("Parameter Server Container", experiment.parameter_server_container),
            ("Parameter Server Count", experiment.parameter_server_count),
            ("Parameter Server Machine Type", experiment.parameter_server_machine_type),
            ("Ports", experiment.ports),
            ("Project ID", experiment.project_id),
            ("Worker Command", experiment.worker_command),
            ("Worker Container", experiment.worker_container),
            ("Worker Count", experiment.worker_count),
            ("Worker Machine Type", experiment.worker_machine_type),
            ("Working Directory", experiment.working_directory),
            ("Workspace URL", experiment.workspace_url),
            ("Tags", tags_string),
        )
        return data

    @staticmethod
    def _get_multi_node_mpi_data(experiment):
        """
        :param api_sdk.MpiMultiNodeExperiment experiment:
        """

        tags_string = ", ".join(experiment.tags)
        data = (
            ("Name", experiment.name),
            ("ID", experiment.id),
            ("State", constants.ExperimentState.get_state_str(experiment.state)),
            ("Artifact directory", experiment.artifact_directory),
            ("Cluster ID", experiment.cluster_id),
            ("Experiment Env", experiment.experiment_env),
            ("Experiment Type", constants.ExperimentType.get_type_str(experiment.experiment_type_id)),
            ("Model Type", experiment.model_type),
            ("Model Path", experiment.model_path),
            ("Master Command", experiment.master_command),
            ("Master Container", experiment.master_container),
            ("Master Count", experiment.master_count),
            ("Master Machine Type", experiment.master_machine_type),
            ("Ports", experiment.ports),
            ("Project ID", experiment.project_id),
            ("Worker Command", experiment.worker_command),
            ("Worker Container", experiment.worker_container),
            ("Worker Count", experiment.worker_count),
            ("Worker Machine Type", experiment.worker_machine_type),
            ("Working Directory", experiment.working_directory),
            ("Workspace URL", experiment.workspace_url),
            ("Tags", tags_string),
        )
        return data


class ExperimentLogsCommand(LogsCommandMixin, BaseExperimentCommand):
    def _make_table(self, logs, experiment_id):
        table_title = "Experiment %s logs" % experiment_id
        table_data = [("JOB ID", "LINE", "MESSAGE")]
        table = terminaltables.AsciiTable(table_data, title=table_title)

        for log in logs:
            table_data.append(self._format_row(experiment_id, log))

        return table.table

    def _get_log_row_string(self, id, log):
        log_msg = "{}\t{}\t{}".format(*self._format_row(id, log))
        return log_msg

    @staticmethod
    def _format_row(experiment_id, log_row):
        return (style(fg="blue", text=experiment_id),
                style(fg="red", text=str(log_row.line)),
                log_row.message)


class DeleteExperimentCommand(BaseExperimentCommand):
    def execute(self, experiment_id, *args, **kwargs):
        self.client.delete(experiment_id)
        self.logger.log("Experiment deleted")


class ExperimentAddTagsCommand(BaseExperimentCommand):
    def execute(self, experiment_id, *args, **kwargs):
        self.client.add_tags(experiment_id, entity=self.entity, **kwargs)
        self.logger.log("Tags added to experiment")


class ExperimentRemoveTagsCommand(BaseExperimentCommand):
    def execute(self, experiment_id, *args, **kwargs):
        self.client.remove_tags(experiment_id, entity=self.entity, **kwargs)
        self.logger.log("Tags removed from experiment")


class GetExperimentMetricsCommand(BaseExperimentCommand):
    def execute(self, experiment_id, start, end, interval, built_in_metrics, *args, **kwargs):
        metrics = self.client.get_metrics(
            experiment_id,
            start=start,
            end=end,
            built_in_metrics=built_in_metrics,
            interval=interval,
        )
        formatted_metrics = json.dumps(metrics, indent=2, sort_keys=True)
        self.logger.log(formatted_metrics)


class StreamExperimentMetricsCommand(StreamMetricsCommand, BaseExperimentCommand):
    pass

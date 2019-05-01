import os
import pydoc
import zipfile
from collections import OrderedDict

import click
import progressbar
import requests
import terminaltables
from requests_toolbelt.multipart import encoder

from paperspace import logger, constants, client, config
from paperspace.commands import CommandBase
from paperspace.exceptions import PresignedUrlUnreachableException, S3UploadFailedException, \
    PresignedUrlAccessDeniedException
from paperspace.logger import log_response
from paperspace.utils import get_terminal_lines

# from clint.textui.progress import Bar as ProgressBar

experiments_api = client.API(config.CONFIG_EXPERIMENTS_HOST, headers=client.default_headers)


class ExperimentCommand(CommandBase):
    def _log_create_experiment(self, response, success_msg_template, error_msg):
        if response.ok:
            j = response.json()
            handle = j["handle"]
            msg = success_msg_template.format(handle)
            self.logger.log(msg)
        else:
            try:
                data = response.json()
                self.logger.log_error_response(data)
            except ValueError:
                self.logger.log(error_msg)


class CreateExperimentCommand(ExperimentCommand):
    def _retrieve_file_paths(self, dirName):

        # setup file paths variable
        file_paths = {}
        exclude = ['.git', '.idea', '.pytest_cache']
        # Read all directory, subdirectories and file lists
        for root, dirs, files in os.walk(dirName, topdown=True):
            dirs[:] = [d for d in dirs if d not in exclude]
            for filename in files:
                # Create the full filepath by using os module.
                relpath = os.path.relpath(root, dirName)
                if relpath == '.':
                    file_path = filename
                else:
                    file_path = os.path.join(os.path.relpath(root, dirName), filename)
                file_paths[file_path] = os.path.join(root, filename)

        # return all paths
        return file_paths

    def _zip_workspace(self, workspace_path):
        if not workspace_path:
            workspace_path = '.'
            zip_file_name = os.path.basename(os.getcwd()) + '.zip'
        else:
            zip_file_name = os.path.basename(workspace_path) + '.zip'

        zip_file_path = os.path.join(workspace_path, zip_file_name)

        if os.path.exists(zip_file_path):
            self.logger.log('Removing existing archive')
            os.remove(zip_file_path)

        file_paths = self._retrieve_file_paths(workspace_path)

        self.logger.log('Creating zip archive: %s' % zip_file_name)
        zip_file = zipfile.ZipFile(zip_file_path, 'w')

        bar = progressbar.ProgressBar(max_value=len(file_paths))

        with zip_file:
            i = 0
            for relpath, abspath in file_paths.items():
                i+=1
                self.logger.debug('Adding %s to archive' % relpath)
                zip_file.write(abspath, arcname=relpath)
                bar.update(i)
        bar.finish()
        self.logger.log('\nFinished creating archive: %s' % zip_file_name)
        return zip_file_path

    def _create_callback(self, encoder_obj):
        bar = progressbar.ProgressBar(max_value=encoder_obj.len)

        def callback(monitor):
            bar.update(monitor.bytes_read)
        return callback

    def _upload_workspace(self, input_data):
        workspace_url = input_data.get('workspaceUrl')
        workspace_path = input_data.get('workspacePath')
        workspace_archive = input_data.get('workspaceArchive')
        if (workspace_archive and workspace_path) or (workspace_archive and workspace_url) or (
                workspace_path and workspace_url):
            raise click.UsageError("Use either:\n\t--workspaceUrl to point repository URL"
                                   "\n\t--workspacePath to point on project directory"
                                   "\n\t--workspaceArchive to point on project ZIP archive"
                                   "\n or neither to use current directory")

        if workspace_url:
            return  # nothing to do

        if workspace_archive:
            archive_path = os.path.abspath(workspace_archive)
        else:
            archive_path = self._zip_workspace(workspace_path)

        file_name = os.path.basename(archive_path)
        s3_upload_data = self._get_upload_data(file_name)
        bucket_name = s3_upload_data['bucket_name']

        self.logger.log('Uploading zipped workspace to S3')

        files = {'file': (archive_path, open(archive_path, 'rb'))}
        fields = OrderedDict(s3_upload_data['fields'])
        fields.update(files)
        s3_encoder = encoder.MultipartEncoder(fields=fields)
        monitor = encoder.MultipartEncoderMonitor(s3_encoder, callback=self._create_callback(s3_encoder))
        s3_response = requests.post(s3_upload_data['url'], data=monitor, headers={'Content-Type': monitor.content_type})
        if not s3_response.ok:
            raise S3UploadFailedException(s3_response)

        self.logger.log('\nUploading completed')

        return 's3://{}/{}'.format(bucket_name, file_name)

    def execute(self, json_):
        workspace_url = self._upload_workspace(json_)
        if workspace_url:
            json_['workspaceUrl'] = workspace_url

        response = self.api.post("/experiments/", json=json_)

        self._log_create_experiment(response,
                                    "New experiment created with handle: {}",
                                    "Unknown error while creating the experiment")

    def _get_upload_data(self, file_name):
        response = self.api.get("/workspace/get_presigned_url", params={'workspaceName': file_name})
        if response.status_code == 404:
            raise PresignedUrlUnreachableException
        if response.status_code == 403:
            raise PresignedUrlAccessDeniedException
        return response.json()


class CreateAndStartExperimentCommand(ExperimentCommand):
    def execute(self, json_):
        response = self.api.post("/experiments/create_and_start/", json=json_)
        self._log_create_experiment(response,
                                    "New experiment created and started with handle: {}",
                                    "Unknown error while creating/starting the experiment")


def start_experiment(experiment_handle, api=experiments_api):
    url = "/experiments/{}/start/".format(experiment_handle)
    response = api.put(url)
    log_response(response, "Experiment started", "Unknown error while starting the experiment")


def stop_experiment(experiment_handle, api=experiments_api):
    url = "/experiments/{}/stop/".format(experiment_handle)
    response = api.put(url)
    log_response(response, "Experiment stopped", "Unknown error while stopping the experiment")


class ListExperimentsCommand(object):
    def __init__(self, api=experiments_api, logger_=logger):
        self.api = api
        self.logger = logger_

    def execute(self, project_handles=None):
        project_handles = project_handles or []
        params = self._get_query_params(project_handles)
        response = self.api.get("/experiments/", params=params)

        try:
            experiments = self._get_experiments_list(response, bool(project_handles))
        except (ValueError, KeyError) as e:
            self.logger.log("Error while parsing response data: {}".format(e))
        else:
            self._log_experiments_list(experiments)

    @staticmethod
    def _get_query_params(project_handles):
        params = {"limit": -1}  # so the API sends back full list without pagination
        for i, handle in enumerate(project_handles):
            key = "projectHandle[{}]".format(i)
            params[key] = handle

        return params

    @staticmethod
    def _make_experiments_list_table(experiments):
        data = [("Name", "Handle", "Status")]
        for experiment in experiments:
            name = experiment["templateHistory"]["params"].get("name")
            handle = experiment["handle"]
            status = constants.ExperimentState.get_state_str(experiment["state"])
            data.append((name, handle, status))

        ascii_table = terminaltables.AsciiTable(data)
        table_string = ascii_table.table
        return table_string

    @staticmethod
    def _get_experiments_list(response, filtered=False):
        if not response.ok:
            raise ValueError("Unknown error")

        data = response.json()["data"]
        if not filtered:  # If filtering by projectHandle response data has different format...
            return data

        experiments = []
        for project_experiments in data:
            for experiment in project_experiments["data"]:
                experiments.append(experiment)
        return experiments

    def _log_experiments_list(self, experiments):
        if not experiments:
            self.logger.log("No experiments found")
        else:
            table_str = self._make_experiments_list_table(experiments)
            if len(table_str.splitlines()) > get_terminal_lines():
                pydoc.pager(table_str)
            else:
                self.logger.log(table_str)


def _make_details_table(experiment):
    if experiment["experimentTypeId"] == constants.ExperimentType.SINGLE_NODE:
        data = (
            ("Name", experiment["templateHistory"]["params"].get("name")),
            ("Handle", experiment.get("handle")),
            ("State", constants.ExperimentState.get_state_str(experiment.get("state"))),
            ("Ports", experiment["templateHistory"]["params"].get("ports")),
            ("Project Handle", experiment["templateHistory"]["params"].get("project_handle")),
            ("Worker Command", experiment["templateHistory"]["params"].get("worker_command")),
            ("Worker Container", experiment["templateHistory"]["params"].get("worker_container")),
            ("Worker Machine Type", experiment["templateHistory"]["params"].get("worker_machine_type")),
            ("Working Directory", experiment["templateHistory"]["params"].get("workingDirectory")),
            ("Workspace URL", experiment["templateHistory"]["params"].get("workspaceUrl")),
            ("Model Type", experiment["templateHistory"]["params"].get("modelType")),
            ("Model Path", experiment["templateHistory"]["params"].get("modelPath")),
        )
    elif experiment["experimentTypeId"] in (constants.ExperimentType.GRPC_MULTI_NODE,
                                            constants.ExperimentType.MPI_MULTI_NODE):
        data = (
            ("Name", experiment["templateHistory"]["params"].get("name")),
            ("Handle", experiment.get("handle")),
            ("State", constants.ExperimentState.get_state_str(experiment.get("state"))),
            ("Artifact directory", experiment["templateHistory"]["params"].get("artifactDirectory")),
            ("Cluster ID", experiment["templateHistory"]["params"].get("clusterId")),
            ("Experiment Env", experiment["templateHistory"]["params"].get("experimentEnv")),
            ("Experiment Type",
             constants.ExperimentType.get_type_str(experiment["templateHistory"]["params"].get("experimentTypeId"))),
            ("Model Type", experiment["templateHistory"]["params"].get("modelType")),
            ("Model Path", experiment["templateHistory"]["params"].get("modelPath")),
            ("Parameter Server Command", experiment["templateHistory"]["params"].get("parameter_server_command")),
            ("Parameter Server Container", experiment["templateHistory"]["params"].get("parameter_server_container")),
            ("Parameter Server Count", experiment["templateHistory"]["params"].get("parameter_server_count")),
            ("Parameter Server Machine Type",
             experiment["templateHistory"]["params"].get("parameter_server_machine_type")),
            ("Ports", experiment["templateHistory"]["params"].get("ports")),
            ("Project Handle", experiment["templateHistory"]["params"].get("project_handle")),
            ("Worker Command", experiment["templateHistory"]["params"].get("worker_command")),
            ("Worker Container", experiment["templateHistory"]["params"].get("worker_container")),
            ("Worker Count", experiment["templateHistory"]["params"].get("worker_count")),
            ("Worker Machine Type", experiment["templateHistory"]["params"].get("worker_machine_type")),
            ("Working Directory", experiment["templateHistory"]["params"].get("workingDirectory")),
            ("Workspace URL", experiment["templateHistory"]["params"].get("workspaceUrl")),
        )
    else:
        raise ValueError("Wrong experiment type: {}".format(experiment["experimentTypeId"]))

    ascii_table = terminaltables.AsciiTable(data)
    table_string = ascii_table.table
    return table_string


def get_experiment_details(experiment_handle, api=experiments_api):
    url = "/experiments/{}/".format(experiment_handle)
    response = api.get(url)
    details = response.content
    if response.ok:
        try:
            experiment = response.json()["data"]
            details = _make_details_table(experiment)
        except (ValueError, KeyError) as e:
            logger.log("Error parsing response data")
            logger.debug(e)

    log_response(response, details, "Unknown error while retrieving details of the experiment")

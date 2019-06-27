import abc

import six

from gradient import config, constants
from gradient.client import API
from gradient.sdk.models import SingleNodeExperiment
from gradient.sdk.serializers import SingleNodeExperimentSchema
from gradient.workspace import S3WorkspaceHandler


@six.add_metaclass(abc.ABCMeta)
class Logger(object):
    @abc.abstractmethod
    def log(self, msg, *args, **kwargs):
        pass

    @abc.abstractmethod
    def warning(self, msg, *args, **kwargs):
        pass

    @abc.abstractmethod
    def error(self, msg, *args, **kwargs):
        pass

    def debug(self, msg, *args, **kwargs):
        pass


class MuteLogger(Logger):
    def log(self, msg, *args, **kwargs):
        pass

    def warning(self, msg, *args, **kwargs):
        pass

    def error(self, msg, *args, **kwargs):
        pass


class ExperimentsClient(object):
    API_URL = config.CONFIG_EXPERIMENTS_HOST

    def __init__(self, api_key, logger=MuteLogger()):
        """

        :type api_key: str
        :type logger: Logger
        """
        self._client = API(self.API_URL, api_key=api_key)
        self.logger = logger

    def create_single_node(self, name, project_id, machine_type, command, ports=None, workspace=None, workspace_archive=None,
                           workspace_url=None, ignore_files=None, working_directory=None, artifact_directory=None,
                           cluster_id=None, experiment_env=None, model_type=None, model_path=None, container=None,
                           container_user=None, registry_username=None,
                           registry_password=None):
        experiment = SingleNodeExperiment(name=name, project_id=project_id, machine_type=machine_type, ports=ports, workspace=workspace,
                                          workspace_archive=workspace_archive, workspace_url=workspace_url,
                                          ignore_files=ignore_files, working_directory=working_directory,
                                          artifact_directory=artifact_directory, cluster_id=cluster_id,
                                          experiment_env=experiment_env, model_type=model_type, model_path=model_path,
                                          container=container,
                                          command=command, container_user=container_user,
                                          registry_username=registry_username, registry_password=registry_password)
        experiment_dict = self._get_experiment_dict(experiment, SingleNodeExperimentSchema)
        experiment_dict["experimentTypeId"] = constants.ExperimentType.SINGLE_NODE
        response = self._client.post("/experiments/", json=experiment_dict)

        if response.ok:
            return response.json()["handle"]
        else:
            raise Exception()

    def _get_experiment_dict(self, experiment, schema_cls):
        experiment_schema = schema_cls()
        experiment_dict = experiment_schema.dump(experiment).data

        workspace_url = self._get_workspace_url(experiment_dict)
        if workspace_url:
            experiment_dict["workspaceUrl"] = workspace_url

        return experiment_dict

    def _get_workspace_url(self, experiment_dict):
        workspace_handler = S3WorkspaceHandler(experiments_api=self._client, logger_=self.logger)
        workspace_url = workspace_handler.handle(experiment_dict)
        return workspace_url


class SdkClient(object):
    def __init__(self, api_key, logger=MuteLogger()):
        """

        :type api_key: str
        :type logger: Logger
        """
        self.experiments = ExperimentsClient(api_key, logger)

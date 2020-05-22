from . import DeploymentsClient, ExperimentsClient, HyperparameterJobsClient, ModelsClient, ProjectsClient, \
    MachinesClient, NotebooksClient, SecretsClient
from .job_client import JobsClient
from .. import logger as sdk_logger


class SdkClient(object):
    def __init__(self, api_key, logger=sdk_logger.MuteLogger()):
        """
        :param str api_key: API key
        :param sdk_logger.Logger logger:
        """
        self.experiments = ExperimentsClient(api_key=api_key, logger=logger)
        self.deployments = DeploymentsClient(api_key=api_key, logger=logger)
        self.hyperparameters = HyperparameterJobsClient(api_key=api_key, logger=logger)
        self.models = ModelsClient(api_key=api_key, logger=logger)
        self.jobs = JobsClient(api_key=api_key, logger=logger)
        self.projects = ProjectsClient(api_key=api_key, logger=logger)
        self.machines = MachinesClient(api_key=api_key, logger=logger)
        self.notebooks = NotebooksClient(api_key=api_key, logger=logger)
        self.secrets = SecretsClient(api_key=api_key, logger=logger)

from . import ModelsClient, ProjectsClient, \
    MachinesClient, NotebooksClient, SecretsClient, DatasetsClient, MachineTypesClient, DatasetVersionsClient, \
    DatasetTagsClient, ClustersClient, StorageProvidersClient
from .workflow_client import WorkflowsClient
from .. import logger as sdk_logger


class SdkClient(object):
    def __init__(self, api_key, logger=sdk_logger.MuteLogger()):
        """
        :param str api_key: API key
        :param sdk_logger.Logger logger:
        """
        self.clusters = ClustersClient(api_key=api_key, logger=logger)
        self.datasets = DatasetsClient(api_key=api_key, logger=logger)
        self.dataset_tags = DatasetTagsClient(api_key=api_key, logger=logger)
        self.dataset_versions = DatasetVersionsClient(
            api_key=api_key, logger=logger)
        self.machine_types = MachineTypesClient(api_key=api_key, logger=logger)
        self.machines = MachinesClient(api_key=api_key, logger=logger)
        self.models = ModelsClient(api_key=api_key, logger=logger)
        self.notebooks = NotebooksClient(api_key=api_key, logger=logger)
        self.projects = ProjectsClient(api_key=api_key, logger=logger)
        self.secrets = SecretsClient(api_key=api_key, logger=logger)
        self.storage_providers = StorageProvidersClient(
            api_key=api_key, logger=logger)
        self.workflows = WorkflowsClient(api_key=api_key, logger=logger)

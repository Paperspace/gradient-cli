from gradient import config
from .base_client import BaseClient
from .. import repositories


class ModelsClient(BaseClient):
    HOST_URL = config.config.CONFIG_HOST

    def list(self, experiment_id=None, project_id=None):
        """Get list of models

        :param str experiment_id: Experiment ID
        :param str project_id: Project ID

        :rtype: list[models.Model]
        """
        models_list = repositories.ListModels(self.client).list(experiment_id=experiment_id, project_id=project_id)
        return models_list

from .base_client import BaseClient
from .. import repositories


class ModelsClient(BaseClient):
    def list(self, experiment_id=None, project_id=None):
        """Get list of models

        :param str experiment_id: Experiment ID
        :param str project_id: Project ID

        :rtype: list[models.Model]
        """
        repository = repositories.ListModels(api_key=self.api_key, logger=self.logger)
        models_list = repository.list(experiment_id=experiment_id, project_id=project_id)
        return models_list

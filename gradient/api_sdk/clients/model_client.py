import json

from .base_client import BaseClient
from .. import repositories, models


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

    def delete(self, model_id):
        """Delete a model

        :param str model_id: Model ID
        """
        repository = repositories.DeleteModel(api_key=self.api_key, logger=self.logger)
        repository.delete(model_id)

    def upload(self, path, name, model_type, model_summary=None, notes=None):
        """Upload model

        :param file path: path to Model
        :param str name: Model name
        :param str model_type: Model Type
        :param dict|None model_summary: Dictionary describing model parameters like loss, accuracy, etc.
        :param str|None notes: Optional model description

        :return: ID of new model
        :rtype: str
        """

        model = models.Model(
            name=name,
            model_type=model_type,
            summary=json.dumps(model_summary) if model_summary else None,
            notes=notes,
        )

        repository = repositories.UploadModel(api_key=self.api_key, logger=self.logger)
        model_id = repository.create(model, path=path)
        return model_id

    def get(self, model_id):
        """Get model instance

        :param str model_id:
        :return: Model instance
        :rtype: models.Model
        """
        repository = repositories.GetModel(api_key=self.api_key, logger=self.logger)
        model = repository.get(model_id=model_id)
        return model

    def get_model_files(self, model_id, links=False, size=False):
        """Get list of models

        :param str model_id: Model ID
        :param bool links: Get links to model files
        :param bool size: Get sizes of each file in bytes

        :rtype: list[models.ModelFile]
        """
        repository = repositories.ListModelFiles(api_key=self.api_key, logger=self.logger)
        models_list = repository.list(model_id=model_id, links=links, size=size)
        return models_list

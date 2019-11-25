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

    def upload(self, file_handler, name, model_type, model_summary=None, notes=None):
        """Upload model

        :param str file_handler:
        :param str name:
        :param str model_type:
        :param dict|None model_summary:
        :param str|None notes:

        :return: ID of new model
        :rtype: str
        """

        model = models.Model(
            name=name,
            model_type=model_type,
            # model_summary=model_summary,
            notes=notes,
        )

        repository = repositories.UploadModel(api_key=self.api_key, logger=self.logger)
        model_id = repository.create(model, file_handler=file_handler)
        return model_id

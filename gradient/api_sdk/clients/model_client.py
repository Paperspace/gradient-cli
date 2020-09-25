import json

from .base_client import BaseClient, TagsSupportMixin
from .. import repositories, models


class ModelsClient(TagsSupportMixin, BaseClient):
    entity = "mlModel"

    def list(self, experiment_id=None, project_id=None, tags=None):
        """Get list of models

        :param str experiment_id: Experiment ID to filter models
        :param str project_id: Project ID to filter models
        :param list[str]|tuple[str] tags: tags to filter models

        :returns: List of Model instances
        :rtype: list[models.Model]
        """
        repository = self.build_repository(repositories.ListModels)
        models_list = repository.list(experiment_id=experiment_id, project_id=project_id, tags=tags)
        return models_list

    def delete(self, model_id):
        """Delete a model

        :param str model_id: Model ID
        """
        repository = self.build_repository(repositories.DeleteModel)
        repository.delete(model_id)

    def upload(self, path, name, model_type, model_summary=None, notes=None, tags=None, project_id=None, cluster_id=None):
        """Upload model

        :param file path: path to Model
        :param str name: Model name
        :param str model_type: Model Type
        :param dict|None model_summary: Dictionary describing model parameters like loss, accuracy, etc.
        :param str|None notes: Optional model description
        :param list[str] tags: List of tags
        :param str|None project_id: ID of a project
        :param str|None cluster_id: ID of a cluster

        :return: ID of new model
        :rtype: str
        """

        model = models.Model(
            name=name,
            model_type=model_type,
            summary=json.dumps(model_summary) if model_summary else None,
            notes=notes,
            project_id=project_id,
        )

        repository = self.build_repository(repositories.UploadModel)
        model_id = repository.create(model, path=path, cluster_id=cluster_id)

        if tags:
            self.add_tags(entity_id=model_id, tags=tags)

        return model_id

    def get(self, model_id):
        """Get model instance

        :param str model_id:
        :return: Model instance
        :rtype: models.Model
        """
        repository = self.build_repository(repositories.GetModel)
        model = repository.get(model_id=model_id)
        return model

    def get_model_files(self, model_id, links=False, size=False):
        """Get list of models

        :param str model_id: Model ID
        :param bool links: Get links to model files
        :param bool size: Get sizes of each file in bytes

        :rtype: list[models.ModelFile]
        """
        repository = self.build_repository(repositories.ListModelFiles)
        models_list = repository.list(model_id=model_id, links=links, size=size)
        return models_list

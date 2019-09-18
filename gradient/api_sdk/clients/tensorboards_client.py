from .base_client import BaseClient
from .. import repositories, models


class TensorboardClient(BaseClient):
    def create(
            self,
            image=None,
            username=None,
            password=None,
            instance_type=None,
            instance_size=None,
            instances_count=None,
            experiments=None,
    ):
        tensorboard = models.Tensorboard(
            image=image,
            username=username,
            password=password,
            instance=models.Instance(
                type=instance_type,
                size=instance_size,
                count=instances_count,
            ),
            experiments=experiments,
        )

        repository = repositories.CreateTensorboard(api_key=self.api_key, logger=self.logger)
        tensorboard_id = repository.create(tensorboard)
        return tensorboard_id

    def get(self, id):
        repository = repositories.GetTensorboard(api_key=self.api_key, logger=self.logger)
        tensorboard = repository.get(id=id)
        return tensorboard

    def list(self):
        repository = repositories.ListTensorboards(api_key=self.api_key, logger=self.logger)
        tensorboards = repository.list()
        return tensorboards

    def add_experiments(self, id, added_experiments):
        repository = repositories.UpdateTensorboard(api_key=self.api_key, logger=self.logger)
        tensorboard = repository.update(id=id, added_experiments=added_experiments)
        return tensorboard

    def remove_experiments(self, id, removed_experiments):
        repository = repositories.UpdateTensorboard(api_key=self.api_key, logger=self.logger)
        tensorboard = repository.update(id=id, removed_experiments=removed_experiments)
        return tensorboard

from .base_client import BaseClient
from .. import models, repositories


class DatasetsClient(BaseClient):

    def list(self, limit=20, offset=0):
        """Get a list of datasets

        :param int limit: Limit results
        :param int offset: Skip results

        :returns: List of datasets
        :rtype: list[models.Dataset]
        """

        repository = self.build_repository(repositories.ListDatasets)
        return repository.list(limit=limit, offset=offset)

    def delete(self, dataset_id):
        """Delete a dataset

        :param str dataset_id: Dataset ID [required]

        :returns:
        :rtype: None
        """

        repository = self.build_repository(repositories.DeleteDataset)
        repository.delete(dataset_id)

    def get(self, dataset_id):
        """Get a dataset

        :param str dataset_id: Dataset ID [required]

        :returns: Dataset
        :rtype: models.Dataset
        """
        repository = self.build_repository(repositories.GetDataset)
        return repository.get(id=dataset_id)

    def get_ref(self, dataset_ref):
        """Get dataset with resolved version by reference

        :param str dataset_ref: Dataset reference [required]

        :returns: Dataset with resolved version
        :rtype: models.DatasetRef
        """
        repository = self.build_repository(repositories.GetDatasetRef)
        return repository.get(id=dataset_ref)

    def create(self, name, storage_provider_id, description=None):
        """Create a new dataset

        :param str name: Name of dataset [required]
        :param str storage_provider_id: Storage provider ID [required]
        :param str description: Brief description of the dataset

        :returns: Dataset ID
        :rtype: str
        """

        dataset = models.Dataset(
            name=name,
            storage_provider_id=storage_provider_id,
            description=description,
        )

        repository = self.build_repository(repositories.CreateDataset)
        return repository.create(dataset)

    def update(self, dataset_id, name=None, description=None):
        """Update an existing dataset

        :param str dataset_id: Dataset ID [required]
        :param str name: Name of dataset
        :param str description: Brief description of the dataset

        :returns:
        :rtype: None
        """

        dataset = models.Dataset(
            name=name,
            description=description
        )

        repository = self.build_repository(repositories.UpdateDataset)
        return repository.update(dataset_id, dataset)

from .base_client import BaseClient
from .. import models, repositories


class DatasetTagsClient(BaseClient):

    def list(self, dataset_id, limit=20, offset=0):
        """Get a list of dataset tags

        :param str dataset_id: Dataset ID [required]
        :param int limit: Limit results
        :param int offset: Skip results

        :returns: List of dataset tags
        :rtype: list[models.DatasetTag]
        """

        repository = self.build_repository(repositories.ListDatasetTags)
        return repository.list(id=dataset_id, limit=limit, offset=offset)

    def delete(self, dataset_tag_id):
        """Delete a dataset tag

        :param str dataset_tag_id: Dataset tag ID (ex: dataset_id:tag) [required]

        :returns:
        :rtype: None
        """

        repository = self.build_repository(repositories.DeleteDatasetTag)
        repository.delete(dataset_tag_id)

    def get(self, dataset_tag_id):
        """Get a dataset tag

        :param str dataset_tag_id: Dataset tag ID (ex: dataset_id:tag) [required]

        :returns: Dataset tag
        :rtype: models.DatasetTag
        """
        repository = self.build_repository(repositories.GetDatasetTag)
        return repository.get(id=dataset_tag_id)

    def set(self, dataset_version_id, name):
        """Set a dataset tag

        :param str dataset_version_id: Dataset version ID (ex: dataset_id:version) [required]
        :param str name: Dataset tag name [required]

        :returns: Dataset tag
        :rtype: models.DatasetTag
        """

        dataset_tag = models.DatasetTag(name=name)

        repository = self.build_repository(repositories.SetDatasetTag)
        return repository.update(dataset_version_id, dataset_tag)

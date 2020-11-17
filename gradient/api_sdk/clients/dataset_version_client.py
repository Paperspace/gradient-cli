from .base_client import BaseClient
from .. import models, repositories


class DatasetVersionsClient(BaseClient):

    def list(self, dataset_id, is_committed=True, limit=20, offset=0):
        """Get list of your dataset versions

        :param str dataset_id: Dataset ID [required]
        :param bool is_committed: Filter versions by commit status
        :param int limit: Limit results
        :param int offset: Skip results

        :returns: List of dataset versions
        :rtype: list[models.DatasetVersion]
        """

        repository = self.build_repository(repositories.ListDatasetVersions)
        return repository.list(id=dataset_id, is_committed=is_committed, limit=limit, offset=offset)

    def delete(self, dataset_version_id):
        """Delete a dataset version

        :param str dataset_version_id: Dataset version ID (ex: dataset_id:version) [required]

        :returns:
        :rtype: None
        """

        repository = self.build_repository(repositories.DeleteDatasetVersion)
        repository.delete(dataset_version_id)

    def get(self, dataset_version_id):
        """Delete a dataset version

        :param str dataset_version_id: Dataset version ID (ex: dataset_id:version) [required]

        :returns: dataset
        :rtype: models.DatasetVersion
        """
        repository = self.build_repository(repositories.GetDatasetVersion)
        return repository.get(id=dataset_version_id)

    def create(self, dataset_id, message=None):
        """Create a new dataset version

        :param str id: Dataset ID [required]
        :param str message: Dataset version message

        :returns: dataset ID
        :rtype: str
        """

        dataset_version = models.DatasetVersion(
            dataset_id=dataset_id,
            message=message,
        )

        repository = self.build_repository(repositories.CreateDatasetVersion)
        return repository.create(dataset_version)

    def update(self, dataset_version_id, message=None, is_committed=None):
        """Update an existing S3 dataset

        :param str dataset_version_id: Dataset version ID (ex: dataset_id:version)
        :param str message: Dataset version message
        :param bool is_committed: Mark dataset version as committed

        :returns:
        :rtype: None
        """

        dataset = models.DatasetVersion(
            message=message,
            is_committed=is_committed,
        )

        repository = self.build_repository(repositories.UpdateDatasetVersion)
        return repository.update(dataset_version_id, dataset)

    def generate_pre_signed_s3_url(self, dataset_version_id, method, params=None):
        """Generate pre-signed URL for S3 storage providers

        :param str dataset_version_id: Dataset version ID (ex: dataset_id:version)
        :param str method: S3 method
        :param dict params: S3 params

        :returns:
        :rtype: DatasetVersionPreSignedURL
        """

        call = {'method': method}
        if params:
            call['params'] = params

        repository = self.build_repository(repositories.GenerateDatasetVersionPreSignedS3Urls)
        results = repository.generate(dataset_version_id, [call])
        return results[0]

    def generate_pre_signed_s3_urls(self, dataset_version_id, calls):
        """Generate pre-signed URLs for S3 storage providers

        :param str dataset_version_id: Dataset version ID (ex: dataset_id:version)
        :param list[dict] calls: List of S3 calls

        :returns:
        :rtype: list[models.DatasetVersionPreSignedURL]
        """

        repository = self.build_repository(repositories.GenerateDatasetVersionPreSignedS3Urls)
        return repository.generate(dataset_version_id, calls)

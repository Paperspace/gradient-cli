from .base_client import BaseClient
from .. import models, repositories


class StorageProvidersClient(BaseClient):

    def list(self, limit=20, offset=0):
        """Get list of your storage providers

        :param int limit: limit of the number results
        :param int offset: skip number of results

        :returns: list of storage providers
        :rtype: list[models.StorageProvider]
        """

        repository = self.build_repository(repositories.ListStorageProviders)
        return repository.list(limit=limit, offset=offset)

    def delete(self, storage_provider_id):
        """Delete a storage provider

        :param int storage_provider_id: ID [required]

        :returns:
        :rtype: None
        """

        repository = self.build_repository(repositories.DeleteStorageProvider)
        repository.delete(storage_provider_id)

    def get(self, storage_provider_id):
        """Delete a storage provider

        :param int storage_provider_id: ID [required]

        :returns: storage provider
        :rtype: models.StorageProvider
        """
        repository = self.build_repository(repositories.GetStorageProvider)
        return repository.get(id=storage_provider_id)

    def create_s3(self, name, bucket, access_key, secret_access_key, endpoint=None, region=None,
                  signature_version=None):
        """Create a new S3 storage provider

        :param str name: Name of new AWS storage provider [required]
        :param str bucket: S3 bucket [required]
        :param str access_key: S3 access key ID [required]
        :param str secret_access_key: S3 access key ID [required]
        :param str endpoint: S3 endpoint URL
        :param str region: S3 region
        :param str signature_version: S3 signature version (ex: v4)

        :returns: storage provider ID
        :rtype: str
        """

        config = {
            'bucket': bucket,
            'accessKey': access_key,
            'secretAccessKey': secret_access_key,
        }
        if endpoint:
            config['endpoint'] = endpoint
        if region:
            config['region'] = region
        if signature_version:
            config['signatureVersion'] = signature_version

        storage_provider = models.StorageProvider(
            type='s3',
            name=name,
            config=config,
        )

        repository = self.build_repository(repositories.CreateStorageProvider)
        return repository.create(storage_provider)

    def update_s3(self, storage_provider_id, name=None, bucket=None, access_key=None, secret_access_key=None,
                  endpoint=None, region=None, signature_version=None):
        """Update an existing S3 storage provider

        :param str storage_provider_id: Storage provider ID
        :param str name: Storage provider name
        :param str bucket: S3 bucket
        :param str access_key: S3 access key ID
        :param str secret_access_key: S3 access key ID
        :param str endpoint: S3 endpoint URL
        :param str region: S3 region
        :param str signature_version: S3 signature version (ex: v4)

        :returns:
        :rtype: None
        """

        config = {}
        if bucket:
            config['bucket'] = bucket
        if access_key:
            config['accessKey'] = access_key
        if secret_access_key:
            config['secretAccessKey'] = secret_access_key
        if endpoint is not None:
            config['endpoint'] = endpoint
        if region is not None:
            config['region'] = region
        if signature_version is not None:
            config['signatureVersion'] = signature_version

        storage_provider = models.StorageProvider(
            name=name,
            config=config,
        )

        repository = self.build_repository(repositories.UpdateStorageProvider)
        return repository.update(storage_provider_id, storage_provider)

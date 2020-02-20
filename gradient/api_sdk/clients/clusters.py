from gradient.api_sdk import repositories

from gradient.api_sdk.clients.base_client import BaseClient


class ClustersClient(BaseClient):
    def list(self, limit=11, offset=0, **kwargs):
        """
        Get a list of clusters for your team

        :param int limit: how many element to return on request
        :param int offset: from what position we should return clusters

        :return: clusters
        :rtype: list
        """
        repository = repositories.ListClusters(api_key=self.api_key, logger=self.logger)
        clusters = repository.list(limit=limit, offset=offset)
        return clusters

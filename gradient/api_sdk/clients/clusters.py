from .base_client import BaseClient
from .. import repositories


class ClustersClient(BaseClient):
    def list(self, limit=11, offset=0, **kwargs):
        """
        Get a list of clusters for your team

        :param int limit: how many element to return on request
        :param int offset: from what position we should return clusters

        :return: clusters
        :rtype: list
        """
        repository = self.build_repository(repositories.ListClusters)
        clusters = repository.list(limit=limit, offset=offset)
        return clusters

from gradient.api_sdk import repositories

from gradient.api_sdk.clients.base_client import BaseClient


class MachineTypesClient(BaseClient):
    def list(self, cluster_id=None):
        repository = self.build_repository(repositories.ListMachineTypes)
        machine_types = repository.list(cluster_id=cluster_id)
        return machine_types

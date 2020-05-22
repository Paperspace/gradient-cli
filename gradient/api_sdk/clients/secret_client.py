from .base_client import BaseClient
from .. import models, repositories
from ...exceptions import ReceivingDataFailedError

SECRET_ENTITIES = ("cluster", "project", "team")


class SecretsClient(BaseClient):
    def _validate_entity(self, entity, entity_id):
        if entity not in SECRET_ENTITIES:
            raise ReceivingDataFailedError("Unknown entity type provided")
        if not entity_id and entity != 'team':
            raise ReceivingDataFailedError("Entity ID is required")

    def list(self, entity, entity_id):
        """List secrets by entity type and ID.

        :param str entity: entity type (ex: team, cluster, project)
        :param str entity_id: entity ID

        :returns: list of secrets
        :rtype: list[models.Secret]
        """
        self._validate_entity(entity, entity_id)

        repository = self.build_repository(repositories.ListSecrets)
        secrets = repository.list(entity=entity, entity_id=entity_id)
        return secrets

    def set(self, entity, entity_id, name, value):
        """Set entity secret.

        :param str entity: entity type (ex: team, cluster, project)
        :param str entity_id: entity ID
        :param str name: secret name
        :param str value: secret value

        :returns:
        :rtype: None
        """
        self._validate_entity(entity, entity_id)

        repository = self.build_repository(repositories.SetSecret)
        repository.set(entity=entity, entity_id=entity_id, name=name, value=value)

    def delete(self, entity, entity_id, name):
        """Delete entity secret.

        :param str entity: entity type (ex: team, cluster, project)
        :param str entity_id: entity ID
        :param str name: secret name

        :returns:
        :rtype: None
        """
        self._validate_entity(entity, entity_id)

        repository = self.build_repository(repositories.DeleteSecret)
        repository.delete(entity=entity, entity_id=entity_id, name=name)

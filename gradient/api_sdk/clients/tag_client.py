from gradient import ReceivingDataFailedError
from gradient.api_sdk.clients.base_client import BaseClient
from gradient.api_sdk.repositories.tags import ListTagRepository, UpdateTagRepository


class TagClient(BaseClient):
    KNOWN_ENTITIES = [
        "project", "job", "notebook", "experiment", "deployment", "mlModel", "machine",
    ]

    def _validate_entities(self, entity):
        """
        Method to validate if passed entity is correct
        :param entity:
        :return:
        """
        if entity not in self.KNOWN_ENTITIES:
            raise ReceivingDataFailedError("Not known entity type provided")

    def add_tags(self, entity_id, entity, tags):
        """
        Add tags to entity.
        :param entity_id:
        :param entity:
        :param tags:
        :return:
        """
        self._validate_entities(entity)

        list_tag_repository = ListTagRepository(api_key=self.api_key, logger=self.logger)
        entity_tags = list_tag_repository.list(entity=entity, entity_ids=[entity_id])

        if entity_tags:
            tags = list(set(entity_tags.get(entity_id) + tags))

        update_tag_repository = UpdateTagRepository(api_key=self.api_key, logger=self.logger)
        update_tag_repository.update(entity=entity, entity_id=entity_id, tags=tags)

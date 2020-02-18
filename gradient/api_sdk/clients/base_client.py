from .. import logger as sdk_logger
from ..repositories.clusters import ValidateClusterRepository
from gradient.api_sdk.sdk_exceptions import GradientSdkError
from ..repositories.tags import ListTagRepository, UpdateTagRepository
from ...exceptions import ReceivingDataFailedError


class BaseClient(object):
    def __init__(
            self, api_key,
            logger=sdk_logger.MuteLogger()
    ):
        """
        Base class. All client classes inherit from it.

        An API key can be created at paperspace.com after you sign in to your account. After obtaining it, you can set
        it in the CLI using the command::

            gradient apiKey XXXXXXXXXXXXXXXXXXX

        or you can provide your API key in any command, for example::

            gradient experiments run ... --apiKey XXXXXXXXXXXXXXXXXXX

        :param str api_key: your API key
        :param sdk_logger.Logger logger:
        """
        self.api_key = api_key
        self.logger = logger

    KNOWN_TAGS_ENTITIES = [
        "project", "job", "notebook", "experiment", "deployment", "mlModel", "machine",
    ]
    entity = ""

    def _validate_entities(self, entity):
        """
        Method to validate if passed entity is correct
        :param entity:
        :return:
        """
        if entity not in self.KNOWN_TAGS_ENTITIES:
            raise ReceivingDataFailedError("Not known entity type provided")

    @staticmethod
    def merge_tags(entity_id, entity_tags, new_tags):
        result_tags = []
        if entity_tags:
            entity_tags = entity_tags[0].get(entity_id, [])

            result_tags = entity_tags + new_tags
        else:
            result_tags += new_tags
        return sorted(list(set(result_tags)))

    @staticmethod
    def diff_tags(entity_id, entity_tags, tags_to_remove):
        result_tags = []
        if entity_tags:
            entity_tags = entity_tags[0].get(entity_id, [])
            entity_tags = set(entity_tags) - set(tags_to_remove)
            result_tags = sorted(list(entity_tags))

        return result_tags

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
            tags = self.merge_tags(entity_id, entity_tags, tags)

        update_tag_repository = UpdateTagRepository(api_key=self.api_key, logger=self.logger)
        update_tag_repository.update(entity=entity, entity_id=entity_id, tags=tags)

    def remove_tags(self, entity_id, entity, tags):
        """
        Remove tags from entity.
        :param str entity_id:
        :param str entity:
        :param list[str] tags: list of tags to remove from entity
        :return:
        """
        self._validate_entities(entity)

        list_tag_repository = ListTagRepository(api_key=self.api_key, logger=self.logger)
        entity_tags = list_tag_repository.list(entity=entity, entity_ids=[entity_id])

        if entity_tags:
            entity_tags = self.diff_tags(entity_id, entity_tags, tags)

            update_tag_repository = UpdateTagRepository(api_key=self.api_key, logger=self.logger)
            update_tag_repository.update(entity=entity, entity_id=entity_id, tags=entity_tags)

    def list_tags(self, entity_ids, entity):
        """
        List tags for entity
        :param list[str] entity_ids:
        :param str entity:
        :return:
        """
        self._validate_entities(entity)

        list_tag_repository = ListTagRepository(api_key=self.api_key, logger=self.logger)
        entity_tags = list_tag_repository.list(entity=entity, entity_ids=entity_ids)
        return entity_tags

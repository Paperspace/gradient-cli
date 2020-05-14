import pytest

from gradient.api_sdk.clients.base_client import BaseClient, TagsSupportMixin


class ClassWithTagsSupportMixin(TagsSupportMixin, BaseClient):
    pass


class TestTagsSupportMixinMethods(object):
    example_entity_tags = [{"some_id": ["test0", "test2", "test1", "test3"]}]

    @pytest.mark.parametrize(
        "entity_id, entity_tags, new_tags, expected_result_tags",
        [
            ("some_id", [], ["test1", "test2"], ["test1", "test2"]),
            ("some_id", [{"some_id": []}], ["test1", "test2"], ["test1", "test2"]),
            ("some_id", [{"some_id": ["test0", "test3"]}], ["test1", "test2"], ["test0", "test1", "test2", "test3"]),
            ("some_id", [{"some_id": ["test1", "test2"]}], ["test1", "test2"], ["test1", "test2"]),
        ]
    )
    def test_merge_tags(self, entity_id, entity_tags, new_tags, expected_result_tags):
        result_tags = ClassWithTagsSupportMixin.merge_tags(entity_id, entity_tags, new_tags)
        assert result_tags == expected_result_tags

    @pytest.mark.parametrize(
        "entity_id, entity_tags, tags_to_remove, expected_result_tags",
        [
            ("some_id", [], ["test1", "test2"], []),
            ("some_id", [{"some_id": []}], ["test1", "test2"], []),
            ("some_id", [{"some_id": ["test1"]}], ["test1", "test2"], []),
            ("some_id", [{"some_id": ["test1", "test3"]}], ["test1", "test2"], ["test3"]),
        ]
    )
    def test_diff_tags(self, entity_id, entity_tags, tags_to_remove, expected_result_tags):
        result_tags = ClassWithTagsSupportMixin.diff_tags(entity_id, entity_tags, tags_to_remove)
        assert result_tags == expected_result_tags

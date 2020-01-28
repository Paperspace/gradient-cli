from .common import AlterResource, ListResources
from .. import config


class UpdateTagRepository(AlterResource):
    def get_request_url(self, **kwargs):
        return "/entityTags/updateTags"

    def _get_api_url(self, use_vpc=False):
        return config.config.CONFIG_HOST

    def _get_request_json(self, instance_dict):
        return {
            "entity": instance_dict.get("entity"),
            "entityId": instance_dict.get("entity_id"),
            "tags": instance_dict.get("tags")
        }

    def update(self, **kwargs):
        self._run(**kwargs)

    def _send_request(self, client, url, json_data=None):
        response = client.put(url, json=json_data)
        return response


class ListTagRepository(ListResources):
    def get_request_url(self, **kwargs):
        return "/entityTags/getTags"

    def _get_api_url(self, use_vpc=False):
        return config.config.CONFIG_HOST

    def _get_request_params(self, kwargs):
        return {
            "entity": kwargs.get("entity"),
            "entityIds": kwargs.get("entity_ids")
        }

    def _parse_object(self, instance_dict):
        instances = []
        for entity in instance_dict:
            entity_tags = []
            for tag in entity:
                entity_tags.append(tag.get("tag").get("name"))
            instances.append({entity: entity_tags})
        return instances

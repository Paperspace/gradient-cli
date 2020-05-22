from .common import BaseRepository, ListResources
from .. import config, serializers


class SecretsMixin(object):
    SERIALIZER_CLS = serializers.SecretSchema

    def _get_api_url(self, **kwargs):
        return config.config.CONFIG_HOST

    def _resource_url(self, **kwargs):
        return "/{}s/secrets/{}".format(kwargs.get("entity"), kwargs.get("name"))
    
    def _get_request_params(self, kwargs):
        params = {}

        entity_id = kwargs.get("entity_id")
        if entity_id:
            params["{}Id".format(kwargs.get("entity"))] = entity_id

        return params


class ListSecrets(SecretsMixin, ListResources):
    def get_request_url(self, **kwargs):
        return "/{}s/secrets".format(kwargs.get("entity"))


class SetSecret(SecretsMixin, BaseRepository):
    def get_request_url(self, **kwargs):
        return self._resource_url(**kwargs)

    def _get_request_json(self, kwargs):
        return {"value": kwargs.get("value")}

    def _send_request(self, client, url, json=None, params=None):
        response = client.put(url, json=json, params=params)
        return response

    def set(self, **kwargs):
        response = self._get(**kwargs)
        self._validate_response(response)


class DeleteSecret(SecretsMixin, BaseRepository):
    def get_request_url(self, **kwargs):
        return self._resource_url(**kwargs)

    def _send_request(self, client, url, json=None, params=None):
        response = client.delete(url, params=params)
        return response

    def delete(self, **kwargs):
        response = self._get(**kwargs)
        self._validate_response(response)
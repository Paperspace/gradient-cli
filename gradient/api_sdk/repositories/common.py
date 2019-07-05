import abc

import six

from ..clients import http_client
from ..exceptions import ResourceFetchingError
from ..utils import MessageExtractor


@six.add_metaclass(abc.ABCMeta)
class BaseRepository(object):
    def __init__(self, api):
        self.api = api

    @abc.abstractmethod
    def get_request_url(self, **kwargs):
        """
        :rtype: str
        """
        pass

    def _get(self, kwargs):
        json_ = self._get_request_json(kwargs)
        params = self._get_request_params(kwargs)
        url = self.get_request_url(**kwargs)
        response = self.api.get(url, json=json_, params=params)
        gradient_response = http_client.GradientResponse.interpret_response(response)

        return gradient_response

    @staticmethod
    def _validate_response(response):
        if not response.ok:
            msg = "Failed to fetch data"
            errors = MessageExtractor().get_message_from_response_data(response.data)
            if errors:
                msg += ": " + errors
            raise ResourceFetchingError(msg)

    def _get_request_json(self, kwargs):
        return None

    def _get_request_params(self, kwargs):
        return None


@six.add_metaclass(abc.ABCMeta)
class ListResources(BaseRepository):
    @abc.abstractmethod
    def _parse_objects(self, data, **kwargs):
        pass

    def list(self, **kwargs):
        response = self._get(kwargs)
        self._validate_response(response)
        instances = self._get_instances(response, **kwargs)
        return instances

    def _get_instances(self, response, **kwargs):
        if not response.data:
            return []

        objects = self._parse_objects(response.data, **kwargs)
        return objects


@six.add_metaclass(abc.ABCMeta)
class GetResource(BaseRepository):
    @abc.abstractmethod
    def _parse_object(self, data, **kwargs):
        pass

    def get(self, **kwargs):
        response = self._get(kwargs)
        self._validate_response(response)
        instance = self._get_instance(response, **kwargs)
        return instance

    def _get_instance(self, response, **kwargs):
        try:
            objects = self._parse_object(response.data, **kwargs)
        except KeyError:
            msg = "Error parsing response data: {}".format(str(response.body))
            raise ResourceFetchingError(msg)

        return objects

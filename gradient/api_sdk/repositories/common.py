import abc

import six

from gradient.utils import MessageExtractor
from ..exceptions import ResourceFetchingError
from ..clients import http_client


@six.add_metaclass(abc.ABCMeta)
class ListResources(object):
    def __init__(self, api):
        self.api = api

    @abc.abstractproperty
    def request_url(self):
        """
        :rtype: str
        """
        pass

    @abc.abstractmethod
    def _parse_objects(self, data, **kwargs):
        pass

    def list(self, **kwargs):
        response = self._get_response(kwargs)
        self._validate_response(response)
        objects = self._get_objects(response, **kwargs)
        return objects

    def _get_response(self, kwargs):
        json_ = self._get_request_json(kwargs)
        params = self._get_request_params(kwargs)
        response = self.api.get(self.request_url, json=json_, params=params)
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

    def _get_objects(self, response, **kwargs):
        if not response.data:
            return []

        objects = self._parse_objects(response.data, **kwargs)
        return objects

    def _get_request_json(self, kwargs):
        return None

    def _get_request_params(self, kwargs):
        return None

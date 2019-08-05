import abc

import six

from ..clients import http_client
from ..exceptions import ResourceFetchingError
from ..utils import MessageExtractor


@six.add_metaclass(abc.ABCMeta)
class BaseRepository(object):
    VALIDATION_ERROR_MESSAGE = "Failed to fetch data"

    def __init__(self, client, *args, **kwargs):
        self.client = client

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
        response = self.client.get(url, json=json_, params=params)
        gradient_response = http_client.GradientResponse.interpret_response(response)

        return gradient_response

    def _validate_response(self, response):
        if not response.ok:
            msg = self.VALIDATION_ERROR_MESSAGE
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


@six.add_metaclass(abc.ABCMeta)
class CreateResource(object):
    SERIALIZER_CLS = None

    def __init__(self, client):
        """
        :param http_client.API client:
        """
        self.client = client

    def create(self, instance):
        instance_dict = self._get_instance_dict(instance)
        response = self._send_create_request(instance_dict)
        self._validate_response(response)
        handle = self._process_response(response)
        return handle

    def _get_instance_dict(self, instance):
        serializer = self._get_serializer()
        serialization_result = serializer.dump(instance)
        instance_dict = serialization_result.data
        if serialization_result.errors:
            raise exceptions.ResourceCreatingDataError(str(serialization_result.errors))
        instance_dict = self._process_instance_dict(instance_dict)
        return instance_dict

    def _get_serializer(self):
        serializer = self.SERIALIZER_CLS()
        return serializer

    def _send_create_request(self, instance_dict):
        url = self._get_create_url()
        response = self.client.post(url, json=instance_dict)
        gradient_response = http_client.GradientResponse.interpret_response(response)
        return gradient_response

    @abc.abstractmethod
    def _get_create_url(self):
        """
        :rtype str"""
        return ""

    @staticmethod
    def _validate_response(response):
        if not response.ok:
            msg = "Failed to create resource"
            errors = MessageExtractor().get_message_from_response_data(response.data)
            if errors:
                msg += ": " + errors
            raise ResourceFetchingError(msg)

    def _process_response(self, response):
        try:
            return self._get_id_from_response(response)
        except Exception as e:
            raise exceptions.ResourceCreatingError(e)

    def _get_id_from_response(self, response):
        handle = response.data["handle"]
        return handle

    def _process_instance_dict(self, instance_dict):
        return instance_dict


@six.add_metaclass(abc.ABCMeta)
class DeleteResource(BaseRepository):
    VALIDATION_ERROR_MESSAGE = "Failed to delete resource"

    def delete(self, id_):
        url = self.get_request_url(id_=id_)

        response = self.api.delete(url)
        self._validate_response(response)


@six.add_metaclass(abc.ABCMeta)
class StartResource(BaseRepository):
    def start(self, id_):
        url = self.get_request_url(id_=id_)
        response = self._send_start_request(url)
        self._validate_response(response)

    def _send_start_request(self, url):
        response = self.client.put(url)
        gradient_response = http_client.GradientResponse.interpret_response(response)
        return gradient_response


@six.add_metaclass(abc.ABCMeta)
class StopResource(BaseRepository):
    def stop(self, id_):
        url = self.get_request_url(id_=id_)
        response = self._send_stop_request(url)
        self._validate_response(response)

    def _send_stop_request(self, url):
        response = self.client.put(url)
        gradient_response = http_client.GradientResponse.interpret_response(response)
        return gradient_response

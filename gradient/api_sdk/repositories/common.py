import abc

import six

from ..clients import http_client
from ..exceptions import ResourceFetchingError, ResourceCreatingDataError, ResourceCreatingError
from ..utils import MessageExtractor


@six.add_metaclass(abc.ABCMeta)
class BaseRepository(object):
    VALIDATION_ERROR_MESSAGE = "Failed to fetch data"

    def __init__(self, api_key, logger):
        self.api_key = api_key
        self.logger = logger

    @abc.abstractmethod
    def get_request_url(self, **kwargs):
        """Get url to the endpoint (without base api url)

        :rtype: str
        """
        pass

    @abc.abstractmethod
    def _get_api_url(self, use_vpc=False):
        """Get base url to the api

        :rtype: str
        """
        pass

    def _get_client(self, use_vpc=False):
        """
        :rtype: http_client.API
        """
        api_url = self._get_api_url(use_vpc=use_vpc)
        client = http_client.API(api_url=api_url, api_key=self.api_key, logger=self.logger)
        return client

    def _get(self, kwargs, use_vpc=False):
        json_ = self._get_request_json(kwargs)
        params = self._get_request_params(kwargs)
        url = self.get_request_url(use_vpc=use_vpc, **kwargs)
        client = self._get_client()
        response = client.get(url, json=json_, params=params)
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
    SERIALIZER_CLS = None

    def _parse_objects(self, data, **kwargs):
        instances = []
        instance_dicts = self._get_instance_dicts(data, **kwargs)
        for instance_dict in instance_dicts:
            instance = self._parse_object(instance_dict)
            instances.append(instance)

        return instances

    def _get_instance_dicts(self, data, **kwargs):
        return data

    def _parse_object(self, instance_dict):
        """
        :param dict instance_dict:
        :return: model instance
        """
        instance = self.SERIALIZER_CLS().get_instance(instance_dict)
        return instance

    def list(self, use_vpc=False, **kwargs):
        response = self._get(kwargs, use_vpc=use_vpc)
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
    SERIALIZER_CLS = None

    def _parse_object(self, instance_dict, **kwargs):
        """
        :param dict instance_dict:
        :return: model instance
        """
        instance = self.SERIALIZER_CLS().get_instance(instance_dict)
        return instance

    def get(self, **kwargs):
        response = self._get(kwargs)
        self._validate_response(response)
        instance = self._get_instance(response, **kwargs)
        return instance

    def _get_instance(self, response, **kwargs):
        try:
            objects = self._parse_object(response.data, **kwargs)
        except Exception:
            msg = "Error parsing response data: {}".format(str(response.body))
            raise ResourceFetchingError(msg)

        return objects


@six.add_metaclass(abc.ABCMeta)
class CreateResource(BaseRepository):
    SERIALIZER_CLS = None
    VALIDATION_ERROR_MESSAGE = "Failed to create resource"
    HANDLE_FIELD = "handle"

    def create(self, instance, use_vpc=False, data=None):
        instance_dict = self._get_instance_dict(instance)
        response = self._send_create_request(instance_dict, use_vpc=use_vpc, data=data)
        self._validate_response(response)
        handle = self._process_response(response)
        return handle

    def _get_instance_dict(self, instance):
        serializer = self._get_serializer()
        serialization_result = serializer.dump(instance)
        instance_dict = serialization_result.data
        if serialization_result.errors:
            raise ResourceCreatingDataError(str(serialization_result.errors))

        instance_dict = self._process_instance_dict(instance_dict)
        return instance_dict

    def _get_serializer(self):
        serializer = self.SERIALIZER_CLS()
        return serializer

    def _send_create_request(self, instance_dict, use_vpc, data=None):
        url = self.get_request_url(use_vpc=use_vpc)
        client = self._get_client(use_vpc=use_vpc)
        json_ = self._get_request_json(instance_dict)
        params = self._get_request_params(instance_dict)
        response = client.post(url, params=params, json=json_, data=data)
        gradient_response = http_client.GradientResponse.interpret_response(response)
        return gradient_response

    def _process_response(self, response):
        try:
            return self._get_id_from_response(response)
        except Exception as e:
            raise ResourceCreatingError(e)

    def _get_id_from_response(self, response):
        handle = response.data[self.HANDLE_FIELD]
        return handle

    def _process_instance_dict(self, instance_dict):
        return instance_dict

    def _get_request_json(self, instance_dict):
        return instance_dict


@six.add_metaclass(abc.ABCMeta)
class AlterResource(BaseRepository):
    def _run(self, use_vpc=False, **kwargs):
        url = self.get_request_url(use_vpc=use_vpc, **kwargs)
        response = self._send(url, use_vpc=use_vpc, **kwargs)
        self._validate_response(response)
        return response

    def _send(self, url, use_vpc=False, **kwargs):
        client = self._get_client(use_vpc=use_vpc)
        json_data = self._get_request_json(kwargs)
        response = self._send_request(client, url, json_data=json_data)
        gradient_response = http_client.GradientResponse.interpret_response(response)
        return gradient_response

    def _send_request(self, client, url, json_data=None):
        response = client.post(url, json=json_data)
        return response


@six.add_metaclass(abc.ABCMeta)
class DeleteResource(AlterResource):
    VALIDATION_ERROR_MESSAGE = "Failed to delete resource"

    def delete(self, id_, use_vpc=False, **kwargs):
        self._run(id=id_, use_vpc=use_vpc, **kwargs)

    def _send_request(self, client, url, json_data=None):
        response = client.delete(url, json=json_data)
        return response


@six.add_metaclass(abc.ABCMeta)
class StartResource(AlterResource):
    VALIDATION_ERROR_MESSAGE = "Unable to start instance"

    def start(self, id_, use_vpc=False):
        self._run(id=id_, use_vpc=use_vpc)

    def _send_request(self, client, url, json_data=None):
        response = client.put(url, json=json_data)
        return response


@six.add_metaclass(abc.ABCMeta)
class StopResource(AlterResource):
    VALIDATION_ERROR_MESSAGE = "Unable to stop instance"

    def stop(self, id_, use_vpc=False):
        self._run(id=id_, use_vpc=use_vpc)

    def _send_request(self, client, url, json_data=None):
        response = client.put(url, json=json_data)
        return response

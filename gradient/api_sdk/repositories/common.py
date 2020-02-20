import abc

import six

from ..clients import http_client
from ..sdk_exceptions import ResourceFetchingError, ResourceCreatingDataError, ResourceCreatingError, GradientSdkError
from ..utils import MessageExtractor


@six.add_metaclass(abc.ABCMeta)
class BaseRepository(object):
    VALIDATION_ERROR_MESSAGE = "Failed to fetch data"

    def __init__(self, api_key, logger, ps_client_name=None):
        self.api_key = api_key
        self.logger = logger
        self.ps_client_name = ps_client_name

    @abc.abstractmethod
    def get_request_url(self, **kwargs):
        """Get url to the endpoint (without base api url)

        :rtype: str
        """
        pass

    @abc.abstractmethod
    def _get_api_url(self, **kwargs):
        """Get base url to the api

        :rtype: str
        """
        pass

    def _get_client(self, **kwargs):
        """
        :rtype: http_client.API
        """
        api_url = self._get_api_url(**kwargs)
        client = http_client.API(
            api_url=api_url,
            api_key=self.api_key,
            logger=self.logger,
            ps_client_name=self.ps_client_name,
        )
        return client

    def _get(self, **kwargs):
        json_ = self._get_request_json(kwargs)
        params = self._get_request_params(kwargs)
        url = self.get_request_url(**kwargs)
        client = self._get_client(**kwargs)
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

    def _get_meta_data(self, resp):
        pass

    def _parse_object(self, instance_dict):
        """
        :param dict instance_dict:
        :return: model instance
        """
        instance = self.SERIALIZER_CLS().get_instance(instance_dict)
        return instance

    def list(self, **kwargs):
        response = self._get(**kwargs)
        self._validate_response(response)
        instances = self._get_instances(response, **kwargs)
        if kwargs.get("get_meta"):
            # Added for now to prevent unnecessary action to update all list commands
            meta_data = self._get_meta_data(response)
            return instances, meta_data
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
        response = self._get(**kwargs)
        self._validate_response(response)
        instance = self._get_instance(response, **kwargs)
        return instance

    def _get_instance(self, response, **kwargs):
        try:
            objects = self._parse_object(response.data, **kwargs)
        except GradientSdkError:
            raise
        except Exception:
            msg = "Error parsing response data: {}".format(str(response.body))
            raise ResourceFetchingError(msg)

        return objects


@six.add_metaclass(abc.ABCMeta)
class CreateResource(BaseRepository):
    SERIALIZER_CLS = None
    VALIDATION_ERROR_MESSAGE = "Failed to create resource"
    HANDLE_FIELD = "handle"

    def create(self, instance, data=None, path=None):
        instance_dict = self._get_instance_dict(instance)
        response = self._send_create_request(instance_dict, data=data, path=path)
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

    def _send_create_request(self, instance_dict, data=None, path=None):
        url = self.get_request_url(**instance_dict)
        client = self._get_client(**instance_dict)
        json_ = self._get_request_json(instance_dict)
        params = self._get_request_params(instance_dict)
        files = self._get_request_files(path)
        response = client.post(url, params=params, json=json_, data=data, files=files)
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

    def _get_request_files(self, path):
        return None


@six.add_metaclass(abc.ABCMeta)
class AlterResource(BaseRepository):
    SERIALIZER_CLS = None

    def update(self, id, instance):
        instance_dict = self._get_instance_dict(instance)
        self._run(id=id, **instance_dict)

    def _get_instance_dict(self, instance):
        serializer = self._get_serializer()
        serialization_result = serializer.dump(instance)
        instance_dict = serialization_result.data
        return instance_dict

    def _get_serializer(self):
        serializer = self.SERIALIZER_CLS()
        return serializer

    def _run(self, **kwargs):
        url = self.get_request_url(**kwargs)
        response = self._send(url, **kwargs)
        self._validate_response(response)
        return response

    def _send(self, url, **kwargs):
        client = self._get_client(**kwargs)
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

    def delete(self, id_, **kwargs):
        self._run(id=id_, **kwargs)

    def _send_request(self, client, url, json_data=None):
        response = client.delete(url, json=json_data)
        return response


@six.add_metaclass(abc.ABCMeta)
class StartResource(AlterResource):
    VALIDATION_ERROR_MESSAGE = "Unable to start instance"

    def start(self, id_):
        self._run(id=id_)

    def _send_request(self, client, url, json_data=None):
        response = client.put(url, json=json_data)
        return response


@six.add_metaclass(abc.ABCMeta)
class StopResource(AlterResource):
    VALIDATION_ERROR_MESSAGE = "Unable to stop instance"

    def stop(self, id_):
        self._run(id=id_)

    def _send_request(self, client, url, json_data=None):
        response = client.put(url, json=json_data)
        return response

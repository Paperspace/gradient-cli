import abc
import collections
import datetime
import json

import dateutil
import six
import websocket

from .. import serializers, sdk_exceptions
from ..clients import http_client
from ..config import config
from ..sdk_exceptions import ResourceFetchingError, ResourceCreatingDataError, ResourceCreatingError, GradientSdkError
from ..utils import MessageExtractor, concatenate_urls


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
        response = self._send_request(client, url, json=json_, params=params)
        gradient_response = http_client.GradientResponse.interpret_response(response)

        return gradient_response

    def _send_request(self, client, url, json=None, params=None):
        response = client.get(url, json=json, params=params)
        return response

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


@six.add_metaclass(abc.ABCMeta)
class GetMetrics(GetResource):
    OBJECT_TYPE = None

    DEFAULT_INTERVAL = "30s"
    DEFAULT_METRICS = ["cpuPercentage", "memoryUsage"]

    @abc.abstractmethod
    def _get_instance_by_id(self, instance_id, **kwargs):
        pass

    def _get_metrics_api_url(self, instance, protocol="https"):
        if not instance.metrics_url:
            raise GradientSdkError("Metrics API url not found")

        metrics_api_url = concatenate_urls(protocol + "://", instance.metrics_url)
        return metrics_api_url

    def _get(self, **kwargs):
        new_kwargs = self._get_kwargs(kwargs)
        rv = super(GetMetrics, self)._get(**new_kwargs)
        return rv

    def _get_kwargs(self, kwargs):
        instance_id = kwargs["id"]
        built_in_metrics = self._get_built_in_metrics_comma_separated(kwargs)
        instance = self._get_instance_by_id(instance_id)
        started_date = self._get_start_date(instance, kwargs)
        end = self._get_end_date(instance, kwargs)
        interval = kwargs.get("interval") or self.DEFAULT_INTERVAL
        metrics_api_url = self._get_metrics_api_url(instance)
        new_kwargs = {
            "charts": built_in_metrics,
            "start": started_date,
            "interval": interval,
            "objecttype": self.OBJECT_TYPE,
            "handle": instance_id,
            "metrics_api_url": metrics_api_url,
        }
        if end:
            new_kwargs["end"] = end

        return new_kwargs

    def get_request_url(self, **kwargs):
        return "metrics/api/v1/range"

    def _get_api_url(self, **kwargs):
        api_url = kwargs["metrics_api_url"]
        return api_url

    def _get_built_in_metrics_comma_separated(self, kwargs):
        metrics_list = self._get_built_in_metrics_list(kwargs)
        metrics_list = ",".join(metrics_list)
        return metrics_list

    def _get_built_in_metrics_list(self, kwargs):
        metrics = kwargs.get("built_in_metrics") or self.DEFAULT_METRICS
        return metrics

    def _get_start_date(self, instance, kwargs):
        datetime_string = kwargs.get("start") or instance.dt_started or instance.dt_created
        if not datetime_string:
            return None

        datetime_string = self._format_datetime(datetime_string)
        return datetime_string

    def _get_end_date(self, instance, kwargs):
        datetime_string = kwargs.get("end")
        if not datetime_string:
            return None

        datetime_string = self._format_datetime(datetime_string)
        return datetime_string

    def _get_request_params(self, kwargs):
        params = kwargs.copy()
        params.pop("metrics_api_url", None)
        return params

    def _parse_object(self, instance_dict, **kwargs):
        charts = instance_dict["charts"]
        return charts

    def _format_datetime(self, some_datetime):
        if not isinstance(some_datetime, datetime.datetime):
            some_datetime = dateutil.parser.parse(some_datetime)

        datetime_str = some_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
        return datetime_str

class ListMetrics(GetResource):
    OBJECT_TYPE = None

    DEFAULT_INTERVAL = "30s"

    @abc.abstractmethod
    def _get_instance_by_id(self, instance_id, **kwargs):
        pass

    def _get_metrics_api_url(self, instance, protocol="https"):
        if not instance.metrics_url:
            raise GradientSdkError("Metrics API url not found")

        metrics_api_url = concatenate_urls(protocol + "://", instance.metrics_url)
        return metrics_api_url

    def _get(self, **kwargs):
        new_kwargs = self._get_kwargs(kwargs)
        rv = super(ListMetrics, self)._get(**new_kwargs)
        return rv

    def _get_kwargs(self, kwargs):
        instance_id = kwargs["id"]
        instance = self._get_instance_by_id(instance_id)
        started_date = self._get_start_date(instance, kwargs)
        end = self._get_end_date(instance, kwargs)
        interval = kwargs.get("interval") or self.DEFAULT_INTERVAL
        metrics_api_url = self._get_metrics_api_url(instance)
        new_kwargs = {
            "start": started_date,
            "interval": interval,
            "objecttype": self.OBJECT_TYPE,
            "handle": instance_id,
            "metrics_api_url": metrics_api_url,
        }
        if end:
            new_kwargs["end"] = end

        return new_kwargs

    def get_request_url(self, **kwargs):
        return "metrics/api/v1/list"

    def _get_api_url(self, **kwargs):
        api_url = kwargs["metrics_api_url"]
        return api_url

    def _get_start_date(self, instance, kwargs):
        datetime_string = kwargs.get("start") or instance.dt_started or instance.dt_created
        if not datetime_string:
            return None

        datetime_string = self._format_datetime(datetime_string)
        return datetime_string

    def _get_end_date(self, instance, kwargs):
        datetime_string = kwargs.get("end")
        if not datetime_string:
            return None

        datetime_string = self._format_datetime(datetime_string)
        return datetime_string

    def _get_request_params(self, kwargs):
        params = kwargs.copy()
        params.pop("metrics_api_url", None)
        return params

    def _parse_object(self, instance_dict, **kwargs):
        chart_names = instance_dict["chart_names"]
        return chart_names

    def _format_datetime(self, some_datetime):
        if not isinstance(some_datetime, datetime.datetime):
            some_datetime = dateutil.parser.parse(some_datetime)

        datetime_str = some_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
        return datetime_str

@six.add_metaclass(abc.ABCMeta)
class StreamMetrics(BaseRepository):
    OBJECT_TYPE = None

    DEFAULT_INTERVAL = "30s"
    DEFAULT_METRICS = ["cpuPercentage", "memoryUsage"]

    def _get_metrics_api_url(self, instance, protocol="https"):
        if not instance.metrics_url:
            raise GradientSdkError("Metrics API url not found")

        metrics_api_url = concatenate_urls(protocol + "://", instance.metrics_url)
        return metrics_api_url

    def _get_api_url(self, **kwargs):
        api_url = kwargs["metrics_api_url"]
        return api_url

    def stream(self, **kwargs):
        while True:
            try:
                connection = self._get_connection(kwargs)
                self._send_chart_descriptor(connection, kwargs)
                stream_generator = self._get_stream_generator(connection)
                for data in stream_generator:
                    self.logger.debug("Metrics data: {}".format(data))
                    yield data
            except websocket.WebSocketConnectionClosedException as e:
                self.logger.debug("WebSocketConnectionClosedException: {}".format(e))
            except sdk_exceptions.EndWebsocketStream:
                return

    def _get_connection(self, kwargs):
        url = self._get_full_url(kwargs)
        self.logger.debug("(Re)opening websocket connection to: {}".format(url))
        ws = websocket.create_connection(url)
        self.logger.debug("Connected")
        return ws

    def _get_full_url(self, kwargs):
        instance_id = kwargs["id"]
        metrics_api_url = self._get_metrics_api_url(instance_id, protocol="wss")
        url = concatenate_urls(metrics_api_url, self.get_request_url())
        return url

    def get_request_url(self, **kwargs):
        return "metrics/api/v1/stream"

    def _get_chart_descriptor(self, kwargs):
        instance_id = kwargs["id"]
        built_in_metrics = self._get_built_in_metrics_list(kwargs)
        interval = kwargs.get("interval") or self.DEFAULT_INTERVAL
        descriptor_json = collections.OrderedDict(
            (
                ("chart_names", built_in_metrics),
                ("handles", [instance_id]),
                ("object_type", self.OBJECT_TYPE),
                ("poll_interval", interval),
            )
        )

        descriptor = json.dumps(descriptor_json)

        return descriptor

    def _get_built_in_metrics_list(self, kwargs):
        metrics = kwargs.get("built_in_metrics") or self.DEFAULT_METRICS
        return metrics

    def _send_chart_descriptor(self, connection, kwargs):
        descriptor = self._get_chart_descriptor(kwargs)
        self.logger.debug("Sending chart descriptor: {}".format(descriptor))
        response = connection.send(descriptor)
        self.logger.debug("Chart descriptor sent. Response: {}".format(response))

    def _get_stream_generator(self, connection):
        return connection

class ListLogs(ListResources):
    @abc.abstractmethod
    def _get_request_params(self, kwargs):
        pass

    def _get_api_url(self, **kwargs):
        return config.CONFIG_LOG_HOST

    def get_request_url(self, **kwargs):
        return "/jobs/logs"

    def yield_logs(self, id, line=1, limit=10000):

        gen = self._get_logs_generator(id, line, limit)
        return gen

    def _get_logs_generator(self, id, line, limit):
        while True:
            logs = self.list(id=id, line=line, limit=limit)

            for log in logs:
                # stop generator - "PSEOF" indicates there are no more logs
                if log.message == "PSEOF":
                    return

                yield log
                line += 1

    def _parse_objects(self, log_rows, **kwargs):
        serializer = serializers.LogRowSchema()
        log_rows = [serializer.get_instance(row) for row in log_rows]
        return log_rows

from .common import ListResources, CreateResource, StartResource, StopResource, DeleteResource, AlterResource, \
    GetResource, GetMetrics, ListMetrics, StreamMetrics, ListLogs
from .. import serializers, config, sdk_exceptions
from ..sdk_exceptions import ResourceFetchingError, MalformedResponseError


class GetBaseDeploymentApiUrlMixin(object):
    def _get_api_url(self, **_):
        return config.config.CONFIG_HOST


class ListDeployments(GetBaseDeploymentApiUrlMixin, ListResources):
    def get_request_url(self, **kwargs):
        return "/deployments/getDeploymentList/"

    def _parse_objects(self, data, **kwargs):
        deployment_dicts = self._get_deployments_dicts_from_json_data(data, kwargs)
        deployments = []

        for deployment_dict in deployment_dicts:
            deployment = serializers.DeploymentSchema().get_instance(deployment_dict)
            deployments.append(deployment)

        return deployments

    @staticmethod
    def _get_deployments_dicts_from_json_data(data, kwargs):
        return data["deploymentList"]

    def _get_request_json(self, kwargs):
        filters = {}
        if kwargs["model_id"]:
            filters["modelId"] = kwargs["model_id"]

        if kwargs["state"]:
            filters["state"] = kwargs["state"]

        if kwargs["project_id"]:
            filters["projectId"] = kwargs["project_id"]

        if filters:
            json_ = {"filter": {"where": {"and": [filters]}}}
        else:
            json_ = {}

        tags = kwargs.get("tags")
        if tags:
            json_["tagFilter"] = tags

        return json_ or None


class CreateDeployment(GetBaseDeploymentApiUrlMixin, CreateResource):
    SERIALIZER_CLS = serializers.DeploymentCreateSchema

    def get_request_url(self, **kwargs):
        if kwargs.get("cluster"):
            return "/deployments/v2/createDeployment/"

        return "/deployments/createDeployment/"

    def _get_id_from_response(self, response):
        handle = response.data["deployment"]["id"]
        return handle


class StartDeployment(GetBaseDeploymentApiUrlMixin, StartResource):
    def get_request_url(self, **kwargs):
        return "/deployments/v2/updateDeployment/"

    def _get_request_json(self, kwargs):
        data = {
            "id": kwargs["id"],
            "isRunning": True,
        }
        return data

    def _send_request(self, client, url, json_data=None):
        response = client.post(url, json=json_data)
        return response


class StopDeployment(GetBaseDeploymentApiUrlMixin, StopResource):
    def get_request_url(self, **kwargs):
        return "/deployments/v2/updateDeployment/"

    def _get_request_json(self, kwargs):
        data = {
            "id": kwargs["id"],
            "isRunning": False,
        }
        return data

    def _send_request(self, client, url, json_data=None):
        response = client.post(url, json=json_data)
        return response


class DeleteDeployment(GetBaseDeploymentApiUrlMixin, DeleteResource):
    def get_request_url(self, **kwargs):
        return "/deployments/v2/deleteDeployment"

    def _get_request_json(self, kwargs):
        data = {
            "id": kwargs["id"],
            "isRunning": False,
        }
        return data

    def _send_request(self, client, url, json_data=None):
        response = client.post(url, json=json_data)
        return response


class UpdateDeployment(GetBaseDeploymentApiUrlMixin, AlterResource):
    SERIALIZER_CLS = serializers.DeploymentSchema
    VALIDATION_ERROR_MESSAGE = "Failed to update resource"

    def update(self, id, instance):
        instance_dict = self._get_instance_dict(instance)
        self._run(id=id, **instance_dict)

    def get_request_url(self, **kwargs):
        return "/deployments/v2/updateDeployment"

    def _get_request_json(self, kwargs):
        # this temporary workaround is here because create and update
        # endpoints have different names for docker args field
        args = kwargs.pop("dockerArgs", None)
        if args:
            kwargs["args"] = args

        j = {
            "id": kwargs.pop("id"),
            "upd": kwargs,
        }
        return j


class GetDeployment(GetBaseDeploymentApiUrlMixin, GetResource):
    SERIALIZER_CLS = serializers.DeploymentSchema

    def get_request_url(self, **kwargs):
        return "/deployments/getDeploymentList/"

    def _get_request_json(self, kwargs):
        deployment_id = kwargs["deployment_id"]
        filter_ = {"where": {"and": [{"id": deployment_id}]}}
        json_ = {"filter": filter_}
        return json_

    def _parse_object(self, instance_dict, **kwargs):
        try:
            instance_dict = instance_dict["deploymentList"][0]
        except KeyError:
            raise MalformedResponseError("Malformed response from API")
        except IndexError:
            raise ResourceFetchingError("Deployment not found")

        return super(GetDeployment, self)._parse_object(instance_dict, **kwargs)


class GetDeploymentMetrics(GetMetrics):
    OBJECT_TYPE = "modelDeployment"

    def _get_instance_by_id(self, instance_id, **kwargs):
        repository = GetDeployment(self.api_key, logger=self.logger, ps_client_name=self.ps_client_name)
        instance = repository.get(deployment_id=instance_id)
        return instance

    def _get_start_date(self, instance, kwargs):
        rv = super(GetDeploymentMetrics, self)._get_start_date(instance, kwargs)
        if rv is None:
            raise sdk_exceptions.GradientSdkError("Deployment job has not started yet")

        return rv

class ListDeploymentMetrics(ListMetrics):
    OBJECT_TYPE = "modelDeployment"

    def _get_instance_by_id(self, instance_id, **kwargs):
        repository = GetDeployment(self.api_key, logger=self.logger, ps_client_name=self.ps_client_name)
        instance = repository.get(deployment_id=instance_id)
        return instance

    def _get_start_date(self, instance, kwargs):
        rv = super(ListDeploymentMetrics, self)._get_start_date(instance, kwargs)
        if rv is None:
            raise sdk_exceptions.GradientSdkError("Deployment job has not started yet")

        return rv

class StreamDeploymentMetrics(StreamMetrics):
    OBJECT_TYPE = "modelDeployment"

    def _get_metrics_api_url(self, instance_id, protocol="https"):
        repository = GetDeployment(api_key=self.api_key, logger=self.logger, ps_client_name=self.ps_client_name)
        deployment = repository.get(deployment_id=instance_id)

        metrics_api_url = super(StreamDeploymentMetrics, self)._get_metrics_api_url(deployment, protocol="wss")
        return metrics_api_url


class ListDeploymentLogs(ListLogs):
    def _get_request_params(self, kwargs):
        params = {
            "deploymentId": kwargs["id"],
            "line": kwargs["line"],
            "limit": kwargs["limit"]
        }
        return params

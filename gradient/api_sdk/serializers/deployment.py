import marshmallow as ma

from gradient.api_sdk import models
from .base import BaseSchema


class DeploymentSchema(BaseSchema):
    MODEL = models.Deployment

    id = ma.fields.Str(dump_to="id", load_from="id")
    name = ma.fields.Str(required=True)
    endpoint = ma.fields.Str()
    api_type = ma.fields.Str(dump_to="apiType", load_from="apiType")

    state = ma.fields.Str()

    model_id = ma.fields.Str(rquired=True, dump_to="modelId", load_from="modelId")
    project_id = ma.fields.Str(dump_to="projectId", load_from="projectId")

    image_url = ma.fields.Str(required=True, dump_to="imageUrl", load_from="imageUrl")
    deployment_type = ma.fields.Str(required=True, dump_to="deploymentType", load_from="deploymentType")
    machine_type = ma.fields.Str(required=True, dump_to="machineType", load_from="machineType")
    instance_count = ma.fields.Int(required=True, dump_to="instanceCount", load_from="instanceCount")
    container_model_path = ma.fields.Str(dump_to="containerModelPath", load_from="containerModelPath")
    image_username = ma.fields.Str(dump_to="imageUsername", load_from="imageUsername")
    image_password = ma.fields.Str(dump_to="imagePassword", load_from="imagePassword")
    image_server = ma.fields.Str(dump_to="imageServer", load_from="imageServer")
    container_url_path = ma.fields.Str(dump_to="containerUrlPath", load_from="containerUrlPath")
    endpoint_url_path = ma.fields.Str(dump_to="endpointUrlPath", load_from="endpointUrlPath")
    method = ma.fields.Str(dump_to="method", load_from="method")
    docker_args = ma.fields.List(ma.fields.Str(), dump_to="dockerArgs", load_from="dockerArgs")
    env = ma.fields.Dict(dump_to="env", load_from="env")
    ports = ma.fields.Str(dump_to="ports", load_from="ports")
    auth_username = ma.fields.Str(dump_to="oauthKey", load_from="oauthKey")
    auth_password = ma.fields.Str(dump_to="oauthSecret", load_from="oauthSecret")
    cluster_id = ma.fields.Str(dump_to="clusterId", load_from="clusterId")
    tags = ma.fields.List(ma.fields.Str(), load_only=True)
    command = ma.fields.Str()

import marshmallow

from .base import BaseSchema
from .. import models


class NotebookSchema(BaseSchema):
    MODEL = models.Notebook

    id = marshmallow.fields.Str()
    vm_type_id = marshmallow.fields.Int(load_from="vmTypeId", dump_to="vmTypeId")
    container_id = marshmallow.fields.Int(load_from="containerId", dump_to="containerId", allow_none=True)
    container_name = marshmallow.fields.Str(load_from="containerName", dump_to="containerName", allow_none=True)
    name = marshmallow.fields.Str()
    cluster_id = marshmallow.fields.Int(load_from="clusterId", dump_to="clusterId")
    registry_username = marshmallow.fields.Str(load_from="registryUsername", dump_to="registryUsername")
    registry_password = marshmallow.fields.Str(load_from="registryPassword", dump_to="registryPassword")
    default_entrypoint = marshmallow.fields.Str(load_from="defaultEntrypoint", dump_to="defaultEntrypoint")
    container_user = marshmallow.fields.Str(load_from="containerUser", dump_to="containerUser")
    shutdown_timeout = marshmallow.fields.Int(load_from="shutdownTimeout", dump_to="shutdownTimeout")
    is_preemptible = marshmallow.fields.Bool(load_from="isPreemptible", dump_to="isPreemptible")
    project_id = marshmallow.fields.Str(load_from="projectHandle", dump_to="projectHandle")
    state = marshmallow.fields.Str()
    vm_type = marshmallow.fields.Str(load_from="vmType", dump_to="vmType")
    fqdn = marshmallow.fields.Str()
    namespace = marshmallow.fields.Str()

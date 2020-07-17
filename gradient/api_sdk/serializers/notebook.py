import copy
import marshmallow

from .base import BaseSchema
from .. import models, utils


class NotebookSchema(BaseSchema):
    MODEL = models.Notebook

    id = marshmallow.fields.Str()
    machine_type = marshmallow.fields.Str(load_from="machineType", dump_to="machineType")
    vm_type_id = marshmallow.fields.Int(load_from="vmTypeId", dump_to="vmTypeId")
    vm_type_label = marshmallow.fields.Str(load_from="vmTypeLabel", dump_to="vmTypeLabel")
    container_id = marshmallow.fields.Int(load_from="containerId", dump_to="containerId", allow_none=True)
    container = marshmallow.fields.Str(load_from="container", dump_to="container", allow_none=True)
    container_name = marshmallow.fields.Str(load_from="containerName", dump_to="containerName", allow_none=True)
    name = marshmallow.fields.Str()
    cluster_id = marshmallow.fields.Str(load_from="clusterId", dump_to="clusterId")
    registry_username = marshmallow.fields.Str(load_from="registryUsername", dump_to="registryUsername")
    registry_password = marshmallow.fields.Str(load_from="registryPassword", dump_to="registryPassword")
    command = marshmallow.fields.Str(load_from="command", dump_to="command")
    default_entrypoint = marshmallow.fields.Str(load_from="defaultEntrypoint", dump_to="defaultEntrypoint")
    container_user = marshmallow.fields.Str(load_from="containerUser", dump_to="containerUser")
    shutdown_timeout = marshmallow.fields.Int(load_from="shutdownTimeout", dump_to="shutdownTimeout")
    is_preemptible = marshmallow.fields.Bool(load_from="isPreemptible", dump_to="isPreemptible")
    is_public = marshmallow.fields.Bool(load_from="isPublic", dump_to="isPublic")
    project_id = marshmallow.fields.Str(load_from="projectId", dump_to="projectId")
    project_handle = marshmallow.fields.Str(load_from="projectHandle", dump_to="projectHandle")
    state = marshmallow.fields.Str()
    token = marshmallow.fields.Str()
    job_error = marshmallow.fields.Str(load_from="jobError", dump_to="jobError")
    job_handle = marshmallow.fields.Str(load_from="jobHandle", dump_to="jobHandle")
    container = marshmallow.fields.Str()
    container_url = marshmallow.fields.Str(load_from="containerUrl", dump_to="containerUrl")
    base_container = marshmallow.fields.Str(load_from="baseContainer", dump_to="baseContainerUrl")
    base_container_url = marshmallow.fields.Str(load_from="baseContainerUrl", dump_to="baseContainerUrl")
    workspace = marshmallow.fields.Str(load_from="workspace", dump_to="workspace")
    workspace_username = marshmallow.fields.Str(load_from="workspaceUsername", dump_to="workspaceUsername")
    workspace_password = marshmallow.fields.Str(load_from="workspacePassword", dump_to="workspacePassword")
    workspace_ref = marshmallow.fields.Str(load_from="workspaceRef", dump_to="workspaceRef")
    vm_type = marshmallow.fields.Str(load_from="vmType", dump_to="vmType")
    fqdn = marshmallow.fields.Str()
    namespace = marshmallow.fields.Str()
    tags = marshmallow.fields.List(marshmallow.fields.Str(), load_only=True)
    metrics_url = marshmallow.fields.Str(dump_to="metricsURL", load_from="metricsURL")
    dt_created = marshmallow.fields.DateTime(dump_to="dtCreated", load_from="dtCreated")
    dt_modified = marshmallow.fields.DateTime(dump_to="dtModified", load_from="dtModified")
    dt_started = marshmallow.fields.DateTime(dump_to="dtStarted", load_from="dtStarted")
    dt_finished = marshmallow.fields.DateTime(dump_to="dtFinished", load_from="dtFinished")
    dt_provisioning_started = marshmallow.fields.Str(dump_to="dtProvisioningStarted", load_from="dtProvisioningStarted")
    dt_provisioning_finished = marshmallow.fields.Str(dump_to="dtProvisioningFinished",
                                                      load_from="dtProvisioningFinished")
    dt_teardown_started = marshmallow.fields.DateTime(dump_to="dtTeardownStarted", load_from="dtTeardownStarted")
    dt_teardown_finished = marshmallow.fields.DateTime(dump_to="dtTeardownStarted", load_from="dtTeardownStarted")
    dt_workspace_upload_finished = marshmallow.fields.DateTime(dump_to="dtWorkspaceUploadFinished", load_from="dtWorkspaceUploadFinished")
    dt_deleted = marshmallow.fields.DateTime(dump_to="dtDeleted", load_from="dtDeleted")
    environment = marshmallow.fields.Dict(dump_to="environment", load_from="environment")

    @marshmallow.pre_dump
    def preprocess(self, data, **kwargs):
        data = copy.copy(data)

        utils.base64_encode_attribute(data, "command")
        return data


class NotebookStartSchema(BaseSchema):
    MODEL = models.NotebookStart

    notebook_id = marshmallow.fields.Str(load_from="notebookId", dump_to="notebookId")
    machine_type = marshmallow.fields.Str(load_from="machineType", dump_to="machineType")
    vm_type_id = marshmallow.fields.Int(load_from="vmTypeId", dump_to="vmTypeId")
    vm_type_label = marshmallow.fields.Str(load_from="vmTypeLabel", dump_to="vmTypeLabel")
    name = marshmallow.fields.Str(load_from="notebookName", dump_to="notebookName")
    cluster_id = marshmallow.fields.Str(load_from="clusterId", dump_to="clusterId")
    shutdown_timeout = marshmallow.fields.Int(load_from="shutdownTimeout", dump_to="shutdownTimeout")
    is_preemptible = marshmallow.fields.Bool(load_from="isPreemptible", dump_to="isPreemptible")

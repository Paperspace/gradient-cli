import marshmallow

from gradient.api_sdk import models
from . import BaseSchema


class _ExperimentSchema(BaseSchema):
    name = marshmallow.fields.Str(required=True)
    ports = marshmallow.fields.Str()
    workspace = marshmallow.fields.Str()
    workspace_archive = marshmallow.fields.Str(dump_to="workspaceArchive")
    workspace_url = marshmallow.fields.Str(dump_to="workspaceUrl")
    ignore_files = marshmallow.fields.List(marshmallow.fields.String(), )
    working_directory = marshmallow.fields.Str(dump_to="workingDirectory")
    artifact_directory = marshmallow.fields.Str(dump_to="artifactDirectory")
    cluster_id = marshmallow.fields.Int(dump_to="clusterId")
    experiment_env = marshmallow.fields.Dict(dump_to="experimentEnv")
    project_id = marshmallow.fields.Str(required=True, dump_to="projectHandle", load_from="projectHandle")
    model_type = marshmallow.fields.Str(dump_to="modelType")
    model_path = marshmallow.fields.Str(dump_to="modelPath")
    id = marshmallow.fields.Str(load_from="handle")
    state = marshmallow.fields.Int()

    def get_instance(self, obj_dict):
        obj_dict.pop("id", None)
        instance = super(_ExperimentSchema, self).get_instance(obj_dict)
        return instance


class SingleNodeExperimentSchema(_ExperimentSchema):
    MODEL = models.SingleNodeExperiment

    experiment_type_id = marshmallow.fields.Int(required=True, dump_to="experimentTypeId")
    container = marshmallow.fields.Str(required=True)
    machine_type = marshmallow.fields.Str(required=True, dump_to="machineType", load_from="machine_type")
    command = marshmallow.fields.Str(required=True)
    container_user = marshmallow.fields.Str(dump_to="containerUser")
    registry_username = marshmallow.fields.Str(dump_to="registryUsername")
    registry_password = marshmallow.fields.Str(dump_to="registryPassword")


class MultiNodeExperimentSchema(_ExperimentSchema):
    MODEL = models.MultiNodeExperiment

    experiment_type_id = marshmallow.fields.Int(required=True, dump_to="experimentTypeId")
    worker_container = marshmallow.fields.Str(required=True, dump_to="workerContainer")
    worker_machine_type = marshmallow.fields.Str(required=True, dump_to="workerMachineType")
    worker_command = marshmallow.fields.Str(required=True, dump_to="workerCommand")
    worker_count = marshmallow.fields.Int(required=True, dump_to="workerCount")
    parameter_server_container = marshmallow.fields.Str(required=True, dump_to="parameterServerContainer")
    parameter_server_machine_type = marshmallow.fields.Str(required=True, dump_to="parameterServerMachineType")
    parameter_server_command = marshmallow.fields.Str(required=True, dump_to="parameterServerCommand")
    parameter_server_count = marshmallow.fields.Int(required=True, dump_to="parameterServerCount")
    worker_container_user = marshmallow.fields.Str(dump_to="workerContainerUser")
    worker_registry_username = marshmallow.fields.Str(dump_to="workerRegistryUsername")
    worker_registry_password = marshmallow.fields.Str(dump_to="workerRegistryPassword")
    parameter_server_container_user = marshmallow.fields.Str(required=True, dump_to="parameterServerContainerUser")
    parameter_server_registry_container_user = marshmallow.fields.Str(dump_to="parameterServerRegistryContainerUser")
    parameter_server_registry_password = marshmallow.fields.Str(dump_to="parameterServerRegistryPassword")

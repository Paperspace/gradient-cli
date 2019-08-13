import marshmallow

from . import BaseSchema
from .. import models


class BaseExperimentSchema(BaseSchema):
    experiment_type_id = marshmallow.fields.Int(required=True, dump_to="experimentTypeId", load_from="experimentTypeId")
    name = marshmallow.fields.Str(required=True)
    ports = marshmallow.fields.Str()
    workspace_url = marshmallow.fields.Str(dump_to="workspaceUrl", load_from="workspaceUrl")
    working_directory = marshmallow.fields.Str(dump_to="workingDirectory", load_from="workingDirectory")
    artifact_directory = marshmallow.fields.Str(dump_to="artifactDirectory", load_from="artifactDirectory")
    cluster_id = marshmallow.fields.String(dump_to="clusterId", load_from="clusterId")
    experiment_env = marshmallow.fields.Dict(dump_to="experimentEnv", load_from="experimentEnv")
    project_id = marshmallow.fields.Str(required=True, dump_to="projectHandle", load_from="project_handle")
    model_type = marshmallow.fields.Str(dump_to="modelType", load_from="modelType")
    model_path = marshmallow.fields.Str(dump_to="modelPath", load_from="modelPath")
    is_preemptible = marshmallow.fields.Bool(dump_to="isPreemptible", load_from="isPreemptible")
    id = marshmallow.fields.Str(load_from="handle")
    state = marshmallow.fields.Int()

    def get_instance(self, obj_dict):
        # without popping these marshmallow wouldn't use load_from
        obj_dict.pop("id", None)
        obj_dict.pop("project_id", None)

        ports = obj_dict.get("ports")
        if isinstance(ports, int):
            obj_dict["ports"] = str(ports)

        instance = super(BaseExperimentSchema, self).get_instance(obj_dict)
        return instance


class SingleNodeExperimentSchema(BaseExperimentSchema):
    MODEL = models.SingleNodeExperiment

    container = marshmallow.fields.Str(required=True, load_from="worker_container")
    machine_type = marshmallow.fields.Str(required=True, dump_to="machineType", load_from="worker_machine_type")
    command = marshmallow.fields.Str(required=True, load_from="worker_command")
    container_user = marshmallow.fields.Str(dump_to="containerUser", load_from="containerUser")
    registry_username = marshmallow.fields.Str(dump_to="registryUsername", load_from="registryUsername")
    registry_password = marshmallow.fields.Str(dump_to="registryPassword", load_from="registryPassword")
    registry_url = marshmallow.fields.Str(dump_to="registryUrl", load_from="registryUrl")


class MultiNodeExperimentSchema(BaseExperimentSchema):
    MODEL = models.MultiNodeExperiment

    worker_container = marshmallow.fields.Str(required=True, dump_to="workerContainer", load_from="workerContainer")
    worker_machine_type = marshmallow.fields.Str(required=True, dump_to="workerMachineType",
                                                 load_from="workerMachineType")
    worker_command = marshmallow.fields.Str(required=True, dump_to="workerCommand", load_from="workerCommand")
    worker_count = marshmallow.fields.Int(required=True, dump_to="workerCount", load_from="workerCount")
    parameter_server_container = marshmallow.fields.Str(required=True, dump_to="parameterServerContainer",
                                                        load_from="parameterServerContainer")
    parameter_server_machine_type = marshmallow.fields.Str(required=True, dump_to="parameterServerMachineType",
                                                           load_from="parameterServerMachineType")
    parameter_server_command = marshmallow.fields.Str(required=True, dump_to="parameterServerCommand",
                                                      load_from="parameterServerCommand")
    parameter_server_count = marshmallow.fields.Int(required=True, dump_to="parameterServerCount",
                                                    load_from="parameterServerCount")
    worker_container_user = marshmallow.fields.Str(dump_to="workerContainerUser", load_from="workerContainerUser")
    worker_registry_username = marshmallow.fields.Str(dump_to="workerRegistryUsername",
                                                      load_from="workerRegistryUsername")
    worker_registry_password = marshmallow.fields.Str(dump_to="workerRegistryPassword",
                                                      load_from="workerRegistryPassword")
    worker_registry_url = marshmallow.fields.Str(dump_to="workerRegistryUrl",
                                                 load_from="workerRegistryUrl")
    parameter_server_container_user = marshmallow.fields.Str(required=True, dump_to="parameterServerContainerUser",
                                                             load_from="parameterServerContainerUser")
    parameter_server_registry_username = marshmallow.fields.Str(dump_to="parameterServerRegistryUsername",
                                                                load_from="parameterServerRegistryUsername")
    parameter_server_registry_password = marshmallow.fields.Str(dump_to="parameterServerRegistryPassword",
                                                                load_from="parameterServerRegistryPassword")
    parameter_server_registry_url = marshmallow.fields.Str(dump_to="parameterServerRegistryUrl",
                                                           load_from="parameterServerRegistryUrl")

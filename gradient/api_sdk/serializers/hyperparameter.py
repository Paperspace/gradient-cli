import copy

import marshmallow

from .experiment import BaseExperimentSchema
from .tag import TagSchema
from .. import models, utils


class HyperparameterSchema(BaseExperimentSchema):
    MODEL = models.Hyperparameter

    tuning_command = marshmallow.fields.Str(dump_to="tuningCommand", load_from="tuningCommand")
    worker_container = marshmallow.fields.Str(dump_to="workerContainer", load_from="workerContainer")
    worker_container_user = marshmallow.fields.Str(dump_to="workerContainerUser", load_from="workerContainerUser")
    worker_machine_type = marshmallow.fields.Str(dump_to="workerMachineType", load_from="workerMachineType")
    worker_command = marshmallow.fields.Str(dump_to="workerCommand", load_from="workerCommand")
    worker_count = marshmallow.fields.Int(dump_to="workerCount", load_from="workerCount")
    use_dockerfile = marshmallow.fields.Bool(dump_to="useDockerfile", load_from="useDockerfile")
    dockerfile_path = marshmallow.fields.Str(dump_to="dockerfilePath", load_from="dockerfilePath")
    worker_registry_username = marshmallow.fields.Str(dump_to="workerRegistryUsername")
    worker_registry_password = marshmallow.fields.Str(dump_to="workerRegistryPassword")

    hyperparameter_server_registry_username = marshmallow.fields.Str(dump_to="hyperparameterServerRegistryUsername",
                                                                     load_from="hyperparameterServerRegistryUsername")
    hyperparameter_server_registry_password = marshmallow.fields.Str(dump_to="hyperparameterServerRegistryPassword",
                                                                     load_from="hyperparameterServerRegistryPassword")
    hyperparameter_server_machine_type = marshmallow.fields.Str(dump_to="hyperparameterServerMachineType",
                                                                load_from="hyperparameterServerMachineType")
    hyperparameter_server_container = marshmallow.fields.Str(dump_to="hyperparameterServerContainer",
                                                             load_from="hyperparameterServerContainer")
    hyperparameter_server_container_user = marshmallow.fields.Str(dump_to="hyperparameterServerContainerUser",
                                                                  load_from="hyperparameterServerContainerUser")
    tags = marshmallow.fields.Nested(TagSchema, only="name", many=True, load_only=True)

    @marshmallow.pre_dump
    def preprocess(self, data, **kwargs):
        data = copy.copy(data)

        utils.base64_encode_attribute(data, "worker_command")
        utils.base64_encode_attribute(data, "tuning_command")
        return data

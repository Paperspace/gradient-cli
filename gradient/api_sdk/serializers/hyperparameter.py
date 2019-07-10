import marshmallow

from .experiment import BaseExperimentSchema
from .. import models


class HyperparameterSchema(BaseExperimentSchema):
    MODEL = models.Hyperparameter

    tuning_command = marshmallow.fields.Str(dump_to="tuningCommand", load_from="tuningCommand")
    worker_container = marshmallow.fields.Str(dump_to="workerContainer", load_from="workerContainer")
    worker_machine_type = marshmallow.fields.Str(dump_to="workerMachineType", load_from="workerMachineType")
    worker_command = marshmallow.fields.Str(dump_to="workerCommand", load_from="workerCommand")
    worker_count = marshmallow.fields.Int(dump_to="workerCount", load_from="workerCount")
    worker_use_dockerfile = marshmallow.fields.Bool(dump_to="useDockerfile", load_from="useDockerfile")
    worker_dockerfile_path = marshmallow.fields.Str(dump_to="dockerfilePath", load_from="dockerfilePath")

    hyperparameter_server_registry_username = marshmallow.fields.Str(dump_to="hyperparameterServerRegistryUsername",
                                                                     load_from="hyperparameterServerRegistryUsername")
    hyperparameter_server_registry_password = marshmallow.fields.Str(dump_to="hyperparameterServerRegistryPassword",
                                                                     load_from="hyperparameterServerRegistryPassword")
    hyperparameter_server_container_user = marshmallow.fields.Str(dump_to="hyperparameterServerContainerUser",
                                                                  load_from="hyperparameterServerContainerUser")

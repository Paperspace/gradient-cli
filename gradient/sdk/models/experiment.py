import attr


@attr.s
class _Experiment(object):
    name = attr.ib(type=str)
    ports = attr.ib(type=str)
    workspace = attr.ib(type=str)
    workspace_archive = attr.ib(type=str)
    workspace_url = attr.ib(type=str)
    ignore_files = attr.ib(type=list)
    working_directory = attr.ib(type=str)
    artifact_directory = attr.ib(type=str)
    cluster_id = attr.ib(type=int)
    experiment_env = attr.ib(type=dict)
    project_id = attr.ib(type=str)
    model_type = attr.ib(type=str)
    model_path = attr.ib(type=str)


@attr.s
class SingleNodeExperiment(_Experiment):
    container = attr.ib(type=str)
    machine_type = attr.ib(type=str)
    command = attr.ib(type=str)
    container_user = attr.ib(type=str)
    registry_username = attr.ib(type=str)
    registry_password = attr.ib(type=str)
    experiment_type_id = attr.ib(type=int, default=1)

    @experiment_type_id.validator
    def experiment_type_id_validator(self, attribute, value):
        if value is not 1:
            raise ValueError("Single node experiment's type must equal 1")


@attr.s
class MultiNodeExperiment(_Experiment):
    experiment_type_id = attr.ib(type=int)
    worker_container = attr.ib(type=str)
    worker_machine_type = attr.ib(type=str)
    worker_command = attr.ib(type=str)
    worker_count = attr.ib(type=str)
    parameter_server_container = attr.ib(type=str)
    parameter_server_machine_type = attr.ib(type=str)
    parameter_server_command = attr.ib(type=str)
    parameter_server_count = attr.ib(type=int)
    worker_container_user = attr.ib(type=str)
    worker_registry_username = attr.ib(type=str)
    worker_registry_password = attr.ib(type=str)
    parameter_server_container_user = attr.ib(type=str)
    parameter_server_registry_container_user = attr.ib(type=str)
    parameter_server_registry_password = attr.ib(type=str)

import attr


@attr.s
class _Experiment(object):
    name = attr.ib(type=str)
    ports = attr.ib(type=list)
    workspace = attr.ib(type=str)
    workspace_archive = attr.ib(type=str)
    workspace_url = attr.ib(type=str)
    ignore_files = attr.ib(type=list)
    working_directory = attr.ib(type=str)
    artifact_directory = attr.ib(type=str)
    cluster_id = attr.ib(type=str)
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

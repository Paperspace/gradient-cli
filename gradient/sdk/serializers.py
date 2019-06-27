import marshmallow
from marshmallow.decorators import post_load, post_dump

from gradient.sdk.models import SingleNodeExperiment


class _ExperimentSchema(marshmallow.Schema):
    name = marshmallow.fields.Str(required=True)
    ports = marshmallow.fields.List(marshmallow.fields.Integer)
    workspace = marshmallow.fields.Str()
    workspace_archive = marshmallow.fields.Str(dump_to="workspaceArchive")
    workspace_url = marshmallow.fields.Str(dump_to="workspaceUrl")
    ignore_files = marshmallow.fields.List(marshmallow.fields.String)
    working_directory = marshmallow.fields.Str(dump_to="workingDirectory")
    artifact_directory = marshmallow.fields.Str(dump_to="artifactDirectory")
    cluster_id = marshmallow.fields.Str(dump_to="clusterId")
    experiment_env = marshmallow.fields.Dict(dump_to="experimentEnv")
    project_id = marshmallow.fields.Str(required=True, dump_to="projectHandle")
    model_type = marshmallow.fields.Str(dump_to="modelType")
    model_path = marshmallow.fields.Str(dump_to="modelPath")

    @post_dump
    def remove_skip_values(self, data):
        return {
            key: value for key, value in data.items()
            if value is not None
        }


class SingleNodeExperimentSchema(_ExperimentSchema):
    container = marshmallow.fields.Str(required=True)
    machine_type = marshmallow.fields.Str(required=True, dump_to="machineType")
    command = marshmallow.fields.Str(required=True)
    container_user = marshmallow.fields.Str(dump_to="containerUser")
    registry_username = marshmallow.fields.Str(dump_to="registryUsername")
    registry_password = marshmallow.fields.Str(dump_to="registryPassword")

    @post_load
    def make_experiment(self, data):
        return SingleNodeExperiment(**data)

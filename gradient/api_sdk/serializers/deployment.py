import marshmallow

from . import BaseSchema


class DeploymentSchema(BaseSchema):
    id_ = marshmallow.fields.Str()
    name = marshmallow.fields.Str(required=True)

    state = marshmallow.fields.Str()

    model_id = marshmallow.fields.Str(rquired=True, dump_to="modelId")
    project_id = marshmallow.fields.Str(dump_to="projectId")

    image_url = marshmallow.fields.Str(required=True, dump_to="imageUrl")
    deployment_type = marshmallow.fields.Str(required=True, dump_to="deploymentType")
    machine_type = marshmallow.fields.Str(required=True, dump_to="machineType")
    instance_count = marshmallow.fields.Int(required=True, dump_to="instanceCount")

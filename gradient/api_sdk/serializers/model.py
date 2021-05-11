import marshmallow

from .base import BaseSchema
from .. import models


class Model(BaseSchema):
    MODEL = models.Model

    id = marshmallow.fields.Str()
    name = marshmallow.fields.Str()
    project_id = marshmallow.fields.Str(dump_to="projectId", load_from="projectId")
    experiment_id = marshmallow.fields.Str(dump_to="experimentId", load_from="experimentId")
    tags = marshmallow.fields.List(marshmallow.fields.Str(), load_only=True)
    model_type = marshmallow.fields.Str(dump_to="modelType", load_from="modelType")
    url = marshmallow.fields.Str()
    model_path = marshmallow.fields.Str(dump_to="modelPath", load_from="modelPath")
    deployment_state = marshmallow.fields.Str(dump_to="deploymentState", load_from="deploymentState")
    summary = marshmallow.fields.Dict()
    detail = marshmallow.fields.Dict()
    notes = marshmallow.fields.Str()
    dataset_ref = marshmallow.fields.Str(dump_to="datasetRef", load_from="datasetRef")


class ModelFileSchema(BaseSchema):
    MODEL = models.ModelFile

    file = marshmallow.fields.Str()
    url = marshmallow.fields.Str()
    size = marshmallow.fields.Int()

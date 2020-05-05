import marshmallow

from .. import models
from .base import BaseSchema


class ArtifactSchema(BaseSchema):
    MODEL = models.Artifact

    file = marshmallow.fields.Str()
    url = marshmallow.fields.Str(required=True)
    size = marshmallow.fields.Int(required=True)

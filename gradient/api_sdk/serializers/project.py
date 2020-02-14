import marshmallow

from .base import BaseSchema
from .. import models


class Project(BaseSchema):
    MODEL = models.Project

    id = marshmallow.fields.Str(dump_to="handle", load_from="handle")
    name = marshmallow.fields.Str()
    repository_name = marshmallow.fields.Str(dump_to="repoName", load_from="repoName")
    repository_url = marshmallow.fields.Str(dump_to="repoUrl", load_from="repoUrl")
    created = marshmallow.fields.DateTime(dump_to="dtCreated", load_from="dtCreated")
    tags = marshmallow.fields.List(marshmallow.fields.Str(), load_only=True)

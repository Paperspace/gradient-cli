import marshmallow

from . import BaseSchema
from .. import models


class Project(BaseSchema):
    MODEL = models.Project

    id = marshmallow.fields.Str()
    name = marshmallow.fields.Str()
    repository_name = marshmallow.fields.Str(dump_to="repoName", load_from="repoName")
    repository_url = marshmallow.fields.Str(dump_to="repoUrl", load_from="repoUrl")

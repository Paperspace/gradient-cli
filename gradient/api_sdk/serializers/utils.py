import marshmallow

from .base import BaseSchema

from .. import models


def paginate_schema(schema):
    class PaginationSchema(BaseSchema):
        MODEL = models.Pagination
        data = marshmallow.fields.Nested(schema, many=True, dump_only=True)
        start_after = marshmallow.fields.String(
            dump_to='startAfter', load_from='startAfter')

    return PaginationSchema()

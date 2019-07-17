from .. import serializers
from ..repositories.common import CreateResource


class CreateProject(CreateResource):
    SERIALIZER_CLS = serializers.Project

    def _get_create_url(self):
        return "/projects/"

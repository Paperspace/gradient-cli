import marshmallow

from .base import BaseSchema

from .. import models
from ..sdk_exceptions import GradientSdkError
from ..serializers import SingleNodeExperimentSchema, MultiNodeExperimentSchema, HyperparameterSchema, \
    MpiMultiNodeExperimentSchema


EXPERIMENT_ID_TO_EXPERIMENT_SERIALIZER_MAPPING = {
    1: SingleNodeExperimentSchema,
    2: MultiNodeExperimentSchema,
    3: MpiMultiNodeExperimentSchema,
    4: HyperparameterSchema,
}


def get_serializer_for_experiment(experiment_dict):
    """
    :param dict experiment_dict:
    :rtype: serializers.BaseExperimentSchema
    """
    experiment_type_id = experiment_dict["experimentTypeId"]

    try:
        serializer = EXPERIMENT_ID_TO_EXPERIMENT_SERIALIZER_MAPPING[experiment_type_id]
    except KeyError as e:
        raise GradientSdkError("No experiment type with ID: {}".format(str(e)))

    return serializer


def paginate_schema(schema):
    class PaginationSchema(BaseSchema):
        MODEL = models.Pagination
        data = marshmallow.fields.Nested(schema, many=True, dump_only=True)
        start_after = marshmallow.fields.String(dump_to='startAfter', load_from='startAfter')

    return PaginationSchema()
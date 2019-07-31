import attr


@attr.s
class Model(object):
    """
    Model class

    :param str id:
    :param str name:
    :param str project_id:
    :param str experiment_id:
    :param list tags:
    :param str model_type:
    :param str url:
    :param str model_path:
    :param str deployment_state:
    :param str summary:
    :param str detail:
    """
    id = attr.ib(type=str, default=None)
    name = attr.ib(type=str, default=None)
    project_id = attr.ib(type=str, default=None)
    experiment_id = attr.ib(type=str, default=None)
    tags = attr.ib(type=list, default=None)
    model_type = attr.ib(type=str, default=None)
    url = attr.ib(type=str, default=None)
    model_path = attr.ib(type=str, default=None)
    deployment_state = attr.ib(type=str, default=None)
    summary = attr.ib(type=dict, default=None)
    detail = attr.ib(type=dict, default=None)

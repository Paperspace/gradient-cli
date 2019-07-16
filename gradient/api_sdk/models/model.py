import attr


@attr.s
class Model(object):
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

import attr


@attr.s
class Deployment(object):
    id_ = attr.ib(type=str, default=None)
    name = attr.ib(type=str, default=None)
    endpoint = attr.ib(type=str, default=None)
    api_type = attr.ib(type=str, default=None)

    state = attr.ib(type=str, default=None)

    model_id = attr.ib(type=str, default=None)
    project_id = attr.ib(type=str, default=None)

    image_url = attr.ib(type=str, default=None)
    deployment_type = attr.ib(type=str, default=None)
    machine_type = attr.ib(type=str, default=None)
    instance_count = attr.ib(type=int, default=None)

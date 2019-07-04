import attr


@attr.s
class Deployment(object):
    id_ = attr.ib(type=str)
    name = attr.ib(type=str)

    state = attr.ib(type=str)

    model_id = attr.ib(type=str)
    project_id = attr.ib(type=str)

    image_url = attr.ib(type=str)
    deployment_type = attr.ib(type=str)
    machine_type = attr.ib(type=str)
    instance_count = attr.ib(type=int)

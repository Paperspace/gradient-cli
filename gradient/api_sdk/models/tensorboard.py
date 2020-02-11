import attr


@attr.s
class Instance(object):
    type = attr.ib(type=str, default=None)
    size = attr.ib(type=str, default=None)
    count = attr.ib(type=int, default=None)


@attr.s
class Tensorboard(object):
    id = attr.ib(type=str, default=None)
    image = attr.ib(type=str, default=None)
    username = attr.ib(type=str, default=None)
    password = attr.ib(type=str, default=None)
    instance = attr.ib(type=Instance, default=None)
    experiments = attr.ib(type=list, default=None)
    url = attr.ib(type=str, default=None)
    state = attr.ib(type=int, default=None)
    tags = attr.ib(type=list, factory=list)

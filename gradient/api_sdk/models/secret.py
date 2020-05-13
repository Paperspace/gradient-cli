import attr


@attr.s
class Secret(object):
    name = attr.ib(type=str, default=None)

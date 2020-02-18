import datetime

import attr


@attr.s
class Tag(object):
    id = attr.ib(type=str, default=None)
    name = attr.ib(type=str, default=None)
    created = attr.ib(type=datetime.datetime, default=None)

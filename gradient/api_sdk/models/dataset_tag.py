import attr


@attr.s
class DatasetVersionSummary(object):
    """
    Dataset version summary class
    """
    version = attr.ib(type=str, default=None)
    message = attr.ib(type=str, default=None)


@attr.s
class DatasetTag(object):
    """
    Dataset version tag class
    """
    name = attr.ib(type=str, default=None)
    version = attr.ib(type=DatasetVersionSummary, factory=DatasetVersionSummary)

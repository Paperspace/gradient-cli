import attr

from .storage_provider import StorageProvider
from .dataset_version import DatasetVersion


@attr.s
class Dataset(object):
    """
    Dataset class
    """
    id = attr.ib(type=str, default=None)
    name = attr.ib(type=str, default=None)
    description = attr.ib(type=str, default=None)
    storage_provider_id = attr.ib(type=str, default=None)
    storage_provider = attr.ib(type=StorageProvider, factory=StorageProvider)


@attr.s
class DatasetRef(Dataset):
    """
    Dataset reference
    """
    version = attr.ib(type=DatasetVersion, factory=DatasetVersion)

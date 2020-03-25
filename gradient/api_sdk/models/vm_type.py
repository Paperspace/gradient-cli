import attr


@attr.s
class VmTypeGpuModel(object):
    label = attr.ib(type=str, default=None)
    model = attr.ib(type=str, default=None)
    memory_in_bytes = attr.ib(type=int, default=None)


@attr.s
class VmType(object):
    label = attr.ib(type=str, default=None)
    kind = attr.ib(type=str, default=None)
    cpu_count = attr.ib(type=int, default=None)
    ram_in_bytes = attr.ib(type=int, default=None)
    gpu_count = attr.ib(type=int, default=None)
    gpu_model = attr.ib(type=VmTypeGpuModel, default=None)
    is_preemptible = attr.ib(type=bool, default=None)
    deployment_type = attr.ib(type=str, default=None)
    deployment_size = attr.ib(type=str, default=None)
    clusters = attr.ib(type=list, factory=list)

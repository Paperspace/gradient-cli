import marshmallow as ma

from .base import BaseSchema
from .. import models


class VmTypeGpuModelSchema(BaseSchema):
    MODEL = models.VmTypeGpuModel

    label = ma.fields.Str()
    model = ma.fields.Str()
    memory_in_bytes = ma.fields.Int(dump_to="memInBytes", load_from="memInBytes")


class VmTypeSchema(BaseSchema):
    MODEL = models.VmType

    label = ma.fields.Str()
    kind = ma.fields.Str()
    cpu_count = ma.fields.Int(dump_to="cpus", load_from="cpus")
    ram_in_bytes = ma.fields.Int(dump_to="ram", load_from="ram")
    gpu_count = ma.fields.Int(dump_to="gpuCount", load_from="gpuCount")
    gpu_model = ma.fields.Nested(VmTypeGpuModelSchema, dump_to="gpuModel", load_from="gpuModel")
    is_preemptible = ma.fields.Bool(dump_to="isPreemptible", load_from="isPreemptible")
    deployment_type = ma.fields.Str(dump_to="deploymentType", load_from="deploymentType")
    deployment_size = ma.fields.Str(dump_to="deploymentSize", load_from="deploymentSize")
    clusters = ma.fields.List(ma.fields.Str())

    @ma.pre_load()
    def preprocess(self, data, **kwargs):
        gpu_model = data["gpuModel"]
        if gpu_model:
            label = gpu_model.get("label")
            if not label or label == "None":
                data["gpuModel"] = None

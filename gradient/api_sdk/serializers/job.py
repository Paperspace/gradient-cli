import json

import marshmallow

from .base import BaseSchema
from .. import models


class JSONField(marshmallow.fields.Field):
    """Field that serializes to json
    """

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None

        return json.dumps(value)

    def _deserialize(self, value, attr, data, **kwargs):
        return value


class JobSchema(BaseSchema):
    MODEL = models.Job

    id = marshmallow.fields.Str(dump_to="id", load_from="id")
    name = marshmallow.fields.Str(required=True)
    state = marshmallow.fields.Str()
    workspace_file_name = marshmallow.fields.Str(dump_to="workspaceFileName", load_from="workspaceFileName")
    working_directory = marshmallow.fields.Str(dump_to="workingDirectory", load_from="workingDirectory")
    artifacts_directory = marshmallow.fields.Str(dump_to="artifactsDirectory", load_from="artifactsDirectory")
    entrypoint = marshmallow.fields.Str()
    project_id = marshmallow.fields.Str(dump_to="projectId", load_from="projectId")
    project = marshmallow.fields.Str()
    container = marshmallow.fields.Str()
    container_url = marshmallow.fields.Str(dump_to="containerUrl", load_from="containerUrl")
    base_container = marshmallow.fields.Str(dump_to="baseContainer", load_from="baseContainer")
    base_container_url = marshmallow.fields.Str(dump_to="baseContainerUrl", load_from="baseContainerUrl")
    machine_type = marshmallow.fields.Str(dump_to="machineType", load_from="machineType")
    cluster = marshmallow.fields.Str()
    cluster_id = marshmallow.fields.Str(dump_to="clusterId", load_from="clusterId")
    usage_rate = marshmallow.fields.Str(dump_to="usageRate", load_from="usageRate")
    started_by_user_id = marshmallow.fields.Str(dump_to="startedByUserId", load_from="startedByUserId")
    parent_job_id = marshmallow.fields.Str(dump_to="parentJobId", load_from="parentJobId")
    job_error = marshmallow.fields.Str(dump_to="jobError", load_from="jobError")
    dt_created = marshmallow.fields.Str(dump_to="dtCreated", load_from="dtCreated")
    dt_modified = marshmallow.fields.Str(dump_to="dtModified", load_from="dtModified")
    dt_provisioning_started = marshmallow.fields.Str(dump_to="dtProvisioningStarted", load_from="dtProvisioningStarted")
    dt_provisioning_finished = marshmallow.fields.Str(dump_to="dtProvisioningFinished",
                                                      load_from="dtProvisioningFinished")
    dt_started = marshmallow.fields.Str(dump_to="dtStarted", load_from="dtStarted")
    dt_finished = marshmallow.fields.Str(dump_to="dtFinished", load_from="dtFinished")
    dt_teardown_started = marshmallow.fields.Str(dump_to="dtTeardownStarted", load_from="dtTeardownStarted")
    dt_teardown_finished = marshmallow.fields.Str(dump_to="dtTeardownFinished", load_from="dtTeardownFinished")
    dt_deleted = marshmallow.fields.Str(dump_to="dtDeleted", load_from="dtDeleted")
    exit_code = marshmallow.fields.Str(dump_to="exitCode", load_from="exitCode")
    queue_position = marshmallow.fields.Str(dump_to="queuePosition", load_from="queuePosition")
    seq_num = marshmallow.fields.Int(dump_to="seqNum", load_from="seqNum")
    storage_region = marshmallow.fields.Str(dump_to="storageRegion", load_from="storageRegion")
    cluster_machine = marshmallow.fields.Str(dump_to="clusterMachine", load_from="clusterMachine")
    fqdn = marshmallow.fields.Str()
    ports = marshmallow.fields.Str()
    is_public = marshmallow.fields.Bool(dump_to="isPublic", load_from="isPublic")
    container_user = marshmallow.fields.Str(dump_to="containerUser", load_from="containerUser")
    has_code = marshmallow.fields.Bool(dump_to="hasCode", load_from="hasCode")
    code_uploaded = marshmallow.fields.Bool(dump_to="codeUploaded", load_from="codeUploaded")
    code_commit = marshmallow.fields.Str(dump_to="codeCommit", load_from="codeCommit")
    run_till_cancelled = marshmallow.fields.Bool(dump_to="runTillCancelled", load_from="runTillCancelled")
    push_on_completion = marshmallow.fields.Bool(dump_to="pushOnCompletion", load_from="pushOnCompletion")
    new_image_name = marshmallow.fields.Str(dump_to="newImageName", load_from="newImageName")
    cpu_hostname = marshmallow.fields.Str(dump_to="cpuHostname", load_from="cpuHostname")
    cpu_count = marshmallow.fields.Int(dump_to="cpuCount", load_from="cpuCount")
    cpu_model = marshmallow.fields.Str(dump_to="cpuModel", load_from="cpuModel")
    cpu_flags = marshmallow.fields.Str(dump_to="cpuFlags", load_from="cpuFlags")
    cpu_mem = marshmallow.fields.Str(dump_to="cpuMem", load_from="cpuMem")
    gpu_name = marshmallow.fields.Str(dump_to="gpuName", load_from="gpuName")
    gpu_serial = marshmallow.fields.Str(dump_to="gpuSerial", load_from="gpuSerial")
    gpu_device = marshmallow.fields.Str(dump_to="gpuDevice", load_from="gpuDevice")
    gpu_driver = marshmallow.fields.Str(dump_to="gpuDriver", load_from="gpuDriver")
    gpu_count = marshmallow.fields.Int(dump_to="gpuCount", load_from="gpuCount")
    gpu_mem = marshmallow.fields.Str(dump_to="gpuMem", load_from="gpuMem")
    tpu_type = marshmallow.fields.Str(dump_to="tpuType", load_from="tpuType")
    tpu_name = marshmallow.fields.Str(dump_to="tpuName", load_from="tpuName")
    tpu_grpc_url = marshmallow.fields.Str(dump_to="tpuGrpcUrl", load_from="tpuGrpcUrl")
    tpu_tf_version = marshmallow.fields.Str(dump_to="tpuTFVersion", load_from="tpuTFVersion")
    tpu_dataset_dir = marshmallow.fields.Str(dump_to="tpuDatasetDir", load_from="tpuDatasetDir")
    tpu_model_dir = marshmallow.fields.Str(dump_to="tpuModelDir", load_from="tpuModelDir")
    target_node_attrs = marshmallow.fields.Dict(dump_to="targetNodeAttrs", load_from="targetNodeAttrs")
    job_env = marshmallow.fields.Dict(dump_to="jobEnv", load_from="jobEnv")
    env_vars = JSONField(dump_to="envVars", load_from="envVars")
    shared_mem_mbytes = marshmallow.fields.Int(dump_to="sharedMemMBytes", load_from="sharedMemMBytes")
    shutdown_timeout = marshmallow.fields.Int(dump_to="shutdownTimeout", load_from="shutdownTimeout")
    is_preemptible = marshmallow.fields.Bool(dump_to="isPreemptible", load_from="isPreemptible")
    metrics_url = marshmallow.fields.Str(dump_to="metricsURL", load_from="metricsURL")
    custom_metrics = marshmallow.fields.Str(dump_to="customMetrics", load_from="customMetrics")
    experiment_id = marshmallow.fields.Str(dump_to="experimentId", load_from="experimentId")

    command = marshmallow.fields.Str()
    use_dockerfile = marshmallow.fields.Bool(dump_to="useDockerfile", load_from="useDockerfile")
    rel_dockerfile_path = marshmallow.fields.Str(dump_to="relDockerfilePath", load_from="relDockerfilePath")
    registry_username = marshmallow.fields.Str(dump_to="registryUsername", load_from="registryUsername")
    registry_password = marshmallow.fields.Str(dump_to="registryPassword", load_from="registryPassword")
    build_only = marshmallow.fields.Bool(dump_to="buildOnly", load_from="buildOnly")

    registry_target = marshmallow.fields.Str(dump_to="registryTarget", load_from="registryTarget")
    registry_target_username = marshmallow.fields.Str(
        dump_to="registryTargetUsername", load_from="registryTargetUsername")
    registry_target_password = marshmallow.fields.Str(
        dump_to="registryTargetPassword", load_from="registryTargetPassword")

    tags = marshmallow.fields.Str(many=True, load_only=True)

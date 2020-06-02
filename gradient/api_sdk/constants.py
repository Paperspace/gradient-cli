import collections


class ExperimentType:
    SINGLE_NODE = 1
    GRPC_MULTI_NODE = 2
    MPI_MULTI_NODE = 3
    HYPERPARAMETER_TUNING = 4

    @classmethod
    def get_type_str(cls, state_int):
        type_strings = {
            1: "single node",
            2: "GRPC multi node",
            3: "MPI multi node",
            4: "Hyperparameter tuning"
        }
        return type_strings.get(state_int, "undefined")


class ExperimentState:
    PENDING = 1
    PROVISIONED = 2
    NETWORK_SETUP = 3
    RUNNING = 4
    STOPPED = 5
    ERROR = 6
    FAILED = 7
    CANCELLED = 8
    NETWORK_TEARDOWN = 9
    CREATED = 10
    PROVISIONING = 11
    NETWORK_SETTING_UP = 12
    NETWORK_TEARING_DOWN = 13
    ABORTING = 14

    @classmethod
    def get_state_str(cls, state_int):
        state_strings = {
            1: "pending",
            2: "provisioned",
            3: "network setup",
            4: "running",
            5: "stopped",
            6: "error",
            7: "failed",
            8: "canceled",
            9: "network teardown",
            10: "created",
            11: "provisioning",
            12: "network setting up",
            13: "network tearing down",
        }
        return state_strings.get(state_int, "undefined")


class Region(object):
    CA1 = "West Coast (CA1)"
    NY2 = "East Coast (NY2)"
    AMS1 = "Europe (AMS1)"


MACHINE_TYPES = (
    "Air", "Standard", "Pro", "Advanced", "GPU+",
    "P4000", "P5000", "P6000", "V100",
    "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10",
)

BILLING_TYPES = ["hourly", "monthly"]


class RunMode:
    RUN_MODE_DEFAULT = 1
    RUN_MODE_PYTHON_COMMAND = 2
    RUN_MODE_SHELL_COMMAND = 3
    RUN_MODE_PYTHON_MODULE = 4


MULTI_NODE_EXPERIMENT_TYPES_MAP = collections.OrderedDict(
    (
        ("GRPC", ExperimentType.GRPC_MULTI_NODE),
        ("MPI", ExperimentType.MPI_MULTI_NODE),
    )
)

DEPLOYMENT_TYPES_MAP = collections.OrderedDict(
    (
        ("TFServing", "TFServing"),
        ("ONNX", "ONNX"),
        ("Custom", "Custom"),
        ("Flask", "Flask"),
        ("TensorRT", "TensorRT"),
    )
)


class ModelTypes:
    ONNX = "ONNX"
    TENSORFLOW = "Tensorflow"
    GENERIC = "Custom"


MODEL_TYPES_MAP = collections.OrderedDict(
    (
        ("Tensorflow", ModelTypes.TENSORFLOW),
        ("ONNX", ModelTypes.ONNX),
        ("Custom", ModelTypes.GENERIC),
    )
)


class ApiTypes:
    REST = "REST"
    GRPC = "GRPC"


class BuiltinMetrics:
    cpu_percentage = "cpuPercentage"
    memory_usage = "memoryUsage"
    gpu_memory_free = "gpuMemoryFree"
    gpu_memory_used = "gpuMemoryUsed"
    gpu_power_draw = "gpuPowerDraw"
    gpu_temp = "gpuTemp"
    gpu_utilization = "gpuUtilization"
    gpu_memory_utilization = "gpuMemoryUtilization"


METRICS_MAP = collections.OrderedDict(
    (
        ("cpuPercentage", BuiltinMetrics.cpu_percentage),
        ("memoryUsage", BuiltinMetrics.memory_usage),
        ("gpuMemoryFree", BuiltinMetrics.gpu_memory_free),
        ("gpuMemoryUsed", BuiltinMetrics.gpu_memory_used),
        ("gpuPowerDraw", BuiltinMetrics.gpu_power_draw),
        ("gpuTemp", BuiltinMetrics.gpu_temp),
        ("gpuUtilization", BuiltinMetrics.gpu_utilization),
        ("gpuMemoryUtilization", BuiltinMetrics.gpu_memory_utilization),
    )
)


class DatasetVolumeKinds:
    DYNAMIC = "dynamic"
    SHARED = "shared"


DATASET_VOLUME_KINDS = collections.OrderedDict(
    (
        ("dynamic", DatasetVolumeKinds.DYNAMIC),
        ("shared", DatasetVolumeKinds.SHARED),
    ),
)


class DeploymentState:
    BUILDING = 1
    PROVISIONING = 2
    STARTING = 3
    RUNNING = 4
    STOPPING = 5
    STOPPED = 6
    ERROR = 7

    @classmethod
    def get_state_str(cls, state_int):
        state_strings = {
            1: "building",
            2: "provisioning",
            3: "starting",
            4: "running",
            5: "stopping",
            6: "stopped",
            7: "error",
        }
        return state_strings.get(state_int, "undefined")

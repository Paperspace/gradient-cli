class ExperimentType:
    SINGLE_NODE = 1
    GRPC_MULTI_NODE = 2
    MPI_MULTI_NODE = 3

    @classmethod
    def get_type_str(cls, state_int):
        type_strings = {
            1: "single node",
            2: "GRPC multi node",
            3: "MPI multi node",
        }
        return type_strings.get(state_int, "undefined")


class ExperimentState:
    CREATED = 1
    PROVISIONED = 2
    NETWORK_SETUP = 3
    RUNNING = 4
    STOPPED = 5
    ERROR = 6
    FAILED = 7
    CANCELLED = 8
    NETWORK_TEARDOWN = 9
    PENDING = 10
    PROVISIONING = 11
    NETWORK_SETTING_UP = 12
    NETWORK_TEARING_DOWN = 13

    @classmethod
    def get_state_str(cls, state_int):
        state_strings = {
            1: "created",
            2: "provisioned",
            3: "network setup",
            4: "running",
            5: "stopped",
            6: "error",
            7: "failed",
            8: "canceled",
            9: "network teardown",
            10: "pending",
            11: "provisioning",
            12: "network setting up",
            13: "network tearing down",
        }
        return state_strings.get(state_int, "undefined")

import attr

from gradient import constants
from .experiment import BaseExperiment


@attr.s
class Hyperparameter(BaseExperiment):
    experiment_type_id = attr.ib(type=int, default=constants.ExperimentType.HYPERPARAMETER_TUNING)
    tuning_command = attr.ib(type=str, default=None)
    worker_container = attr.ib(type=str, default=None)
    worker_machine_type = attr.ib(type=str, default=None)
    worker_command = attr.ib(type=str, default=None)
    worker_count = attr.ib(type=int, default=None)
    worker_use_dockerfile = attr.ib(type=bool, default=None)
    worker_dockerfile_path = attr.ib(type=str, default=None)

    hyperparameter_server_registry_username = attr.ib(type=str, default=None)
    hyperparameter_server_registry_password = attr.ib(type=str, default=None)
    hyperparameter_server_container_user = attr.ib(type=str, default=None)

    is_preemptible = attr.ib(type=bool, default=None)
    trigger_event_id = attr.ib(type=str, default=None)
    dockerfile_path = attr.ib(type=str, default=None)
    registry_username = attr.ib(type=str, default=None)
    registry_password = attr.ib(type=str, default=None)
    container_user = attr.ib(type=str, default=None)
    use_dockerfile = attr.ib(type=False, default=None)

    @experiment_type_id.validator
    def experiment_type_id_validator(self, attribute, value):
        if value is not constants.ExperimentType.HYPERPARAMETER_TUNING:
            raise ValueError("Hyperparameter tuning model's type must equal {}".
                             format(constants.ExperimentType.HYPERPARAMETER_TUNING))

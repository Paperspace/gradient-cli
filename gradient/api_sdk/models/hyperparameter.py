import attr

from gradient import constants
from .experiment import BaseExperiment


@attr.s
class Hyperparameter(BaseExperiment):
    """
    Hyperparameter job class. Inherits from ``BaseExperiment`` class

    :param int experiment_type_id:
    :param str tuning_command:
    :param str worker_container:
    :param str worker_machine_type:
    :param str worker_command:
    :param int worker_count:
    :param bool worker_use_dockerfile:
    :param str worker_dockerfile_path:
    :param str hyperparameter_server_registry_username:
    :param str hyperparameter_server_registry_password:
    :param str hyperparameter_server_container_user:
    :param bool is_preemptible:
    :param str trigger_event_id:
    :param str dockerfile_path:
    :param str registry_username:
    :param str registry_password:
    :param str container_user:
    :param bool use_dockerfile:
    """
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
    use_dockerfile = attr.ib(type=bool, default=None)

    @experiment_type_id.validator
    def experiment_type_id_validator(self, attribute, value):
        if value is not constants.ExperimentType.HYPERPARAMETER_TUNING:
            raise ValueError("Hyperparameter tuning model's type must equal {}".
                             format(constants.ExperimentType.HYPERPARAMETER_TUNING))

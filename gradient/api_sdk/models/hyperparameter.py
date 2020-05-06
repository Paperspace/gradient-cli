import attr

from .experiment import BaseExperiment
from .. import constants


@attr.s
class Hyperparameter(BaseExperiment):
    """
    Hyperparameter job class. Inherits from ``BaseExperiment`` class

    :param int experiment_type_id: experiment type, for hyperparameter experiment set to 4
    :param str tuning_command: Tuning command
    :param str worker_container: Worker container
    :param str worker_machine_type: Worker machine type
    :param str worker_command: Worker command
    :param int worker_count: Worker count
    :param bool worker_use_dockerfile: Flag: use dockerfile
    :param str worker_dockerfile_path: path to dockerfile, if not set default is project root directory
    :param str worker_container_user: Worker container user
    :param str worker_registry_username: Worker registry username
    :param str worker_registry_password: Worker registry password

    :param str hyperparameter_server_machine_type: Hyperparameter server  machine type
    :param str hyperparameter_server_container: Hyperparameter server container
    :param str hyperparameter_server_container_user: Hyperparameter server container user
    :param str hyperparameter_server_registry_username: Hyperparameter server registry username
    :param str hyperparameter_server_registry_password: Hyperparameter server registry password
    :param bool is_preemptible: Flag: is preemptible
    :param str trigger_event_id: GradientCI trigger event id
    :param str dockerfile_path: Path to dockerfile
    :param bool use_dockerfile: Flag: use dockerfile
    """
    experiment_type_id = attr.ib(type=int, default=constants.ExperimentType.HYPERPARAMETER_TUNING)
    tuning_command = attr.ib(type=str, default=None)
    worker_container = attr.ib(type=str, default=None)
    worker_machine_type = attr.ib(type=str, default=None)
    worker_command = attr.ib(type=str, default=None)
    worker_count = attr.ib(type=int, default=None)
    worker_use_dockerfile = attr.ib(type=bool, default=None)
    worker_dockerfile_path = attr.ib(type=str, default=None)
    worker_container_user = attr.ib(type=str, default=None)
    worker_registry_username = attr.ib(type=str, default=None)
    worker_registry_password = attr.ib(type=str, default=None)

    hyperparameter_server_machine_type = attr.ib(type=str, default=None)
    hyperparameter_server_container = attr.ib(type=str, default=None)
    hyperparameter_server_container_user = attr.ib(type=str, default=None)
    hyperparameter_server_registry_username = attr.ib(type=str, default=None)
    hyperparameter_server_registry_password = attr.ib(type=str, default=None)

    is_preemptible = attr.ib(type=bool, default=None)
    trigger_event_id = attr.ib(type=str, default=None)
    dockerfile_path = attr.ib(type=str, default=None)
    use_dockerfile = attr.ib(type=bool, default=None)
    tags = attr.ib(type=list, factory=list)

    @experiment_type_id.validator
    def experiment_type_id_validator(self, attribute, value):
        if value is not constants.ExperimentType.HYPERPARAMETER_TUNING:
            raise ValueError("Hyperparameter tuning model's type must equal {}".
                             format(constants.ExperimentType.HYPERPARAMETER_TUNING))

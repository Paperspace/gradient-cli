import re

import click

from gradient.api_sdk import constants

REQUIRED_PARAMS_PER_EXPERIMENT_TYPE = {
    constants.ExperimentType.GRPC_MULTI_NODE: ["parameter_server_container", "parameter_server_machine_type",
                                               "parameter_server_command", "parameter_server_count"],
    constants.ExperimentType.MPI_MULTI_NODE: ["master_container", "master_machine_type", "master_command",
                                              "master_count"],
}


def validate_mutually_exclusive(options_1, options_2, error_message):
    used_option_in_options_1 = any(option is not None for option in options_1)
    used_option_in_options_2 = any(option is not None for option in options_2)
    if used_option_in_options_1 and used_option_in_options_2:
        raise click.UsageError(error_message)


def validate_email(ctx, param, value):
    if value is not None \
            and not re.match(r"[^@]+@[^@]+\.[^@]+", value):
        raise click.BadParameter("Bad email address format")

    return value


def validate_multi_node(params):
    experiment_type = params.get('experiment_type_id')
    required_params = REQUIRED_PARAMS_PER_EXPERIMENT_TYPE.get(experiment_type)

    for param_name in required_params:
        if not params.get(param_name):
            raise click.UsageError("Param %s is required for this experiment type" % param_name)

import mock
from click.testing import CliRunner

from paperspace import cli, constants


@mock.patch("paperspace.cli.commands")
def test_should_execute_create_experiment_command_when_cli_singlenode_command_was_executed(commands_patched):
    runner = CliRunner()
    command = "experiments create singlenode " \
              "--name exp1 " \
              "--projectHandle testHandle " \
              "--container testContainer " \
              "--machineType testType " \
              "--command testCommand"
    expected_kwargs = {"name": u"exp1",
                       "projectHandle": u"testHandle",
                       "container": u"testContainer",
                       "machineType": u"testType",
                       "command": u"testCommand",
                       "experimentTypeId": constants.ExperimentType.SINGLE_NODE,
                       }

    result = runner.invoke(cli.cli, command.split())

    assert result.exit_code == 0
    commands_patched.create_experiment.assert_called_once_with(expected_kwargs)


@mock.patch("paperspace.cli.commands")
def test_should_execute_create_experiment_command_when_cli_multinode_mpi_command_was_executed(commands_patched):
    runner = CliRunner()
    command = "experiments create multinode " \
              "--name exp1 " \
              "--projectHandle testHandle " \
              "--experimentTypeId MPI " \
              "--workerContainer testWorkerContainer " \
              "--workerMachineType testWorkerMachineType " \
              "--workerCommand testWorkerCommand " \
              "--workerCount 2 " \
              "--parameterServerContainer testParameterServerContainer " \
              "--parameterServerMachineType testParameterServerMachineType " \
              "--parameterServerCommand testParameterServerCommand " \
              "--parameterServerCount 3"
    expected_kwargs = {"name": u"exp1",
                       "projectHandle": u"testHandle",
                       "experimentTypeId": constants.ExperimentType.MPI_MULTI_NODE,
                       "workerContainer": u"testWorkerContainer",
                       "workerMachineType": u"testWorkerMachineType",
                       "workerCommand": u"testWorkerCommand",
                       "workerCount": 2,
                       "parameterServerContainer": u"testParameterServerContainer",
                       "parameterServerMachineType": u"testParameterServerMachineType",
                       "parameterServerCommand": u"testParameterServerCommand",
                       "parameterServerCount": 3,
                       }

    result = runner.invoke(cli.cli, command.split())

    assert result.exit_code == 0
    commands_patched.create_experiment.assert_called_once_with(expected_kwargs)


@mock.patch("paperspace.cli.commands")
def test_should_execute_create_experiment_command_when_cli_multinode_grpc_command_was_executed(commands_patched):
    runner = CliRunner()
    command = "experiments create multinode " \
              "--name exp1 " \
              "--projectHandle testHandle " \
              "--experimentTypeId GRPC " \
              "--workerContainer testWorkerContainer " \
              "--workerMachineType testWorkerMachineType " \
              "--workerCommand testWorkerCommand " \
              "--workerCount 2 " \
              "--parameterServerContainer testParameterServerContainer " \
              "--parameterServerMachineType testParameterServerMachineType " \
              "--parameterServerCommand testParameterServerCommand " \
              "--parameterServerCount 3"
    expected_kwargs = {"name": u"exp1",
                       "projectHandle": u"testHandle",
                       "experimentTypeId": constants.ExperimentType.GRPC_MULTI_NODE,
                       "workerContainer": u"testWorkerContainer",
                       "workerMachineType": u"testWorkerMachineType",
                       "workerCommand": u"testWorkerCommand",
                       "workerCount": 2,
                       "parameterServerContainer": u"testParameterServerContainer",
                       "parameterServerMachineType": u"testParameterServerMachineType",
                       "parameterServerCommand": u"testParameterServerCommand",
                       "parameterServerCount": 3,
                       }

    result = runner.invoke(cli.cli, command.split())

    assert result.exit_code == 0
    commands_patched.create_experiment.assert_called_once_with(expected_kwargs)


@mock.patch("paperspace.cli.commands")
def test_should_execute_create_experiment_command_when_cli_create_and_start_singlenode_command_was_executed(
        commands_patched):
    runner = CliRunner()
    command = "experiments createAndStart singlenode " \
              "--name exp1 " \
              "--projectHandle testHandle " \
              "--container testContainer " \
              "--machineType testType " \
              "--command testCommand"
    expected_kwargs = {"name": u"exp1",
                       "projectHandle": u"testHandle",
                       "container": u"testContainer",
                       "machineType": u"testType",
                       "command": u"testCommand",
                       "experimentTypeId": constants.ExperimentType.SINGLE_NODE,
                       }

    result = runner.invoke(cli.cli, command.split())

    assert result.exit_code == 0
    commands_patched.create_and_start_experiment.assert_called_once_with(expected_kwargs)


@mock.patch("paperspace.cli.commands")
def test_should_execute_create_experiment_command_when_cli_create_and_start_multinode_mpi_command_was_executed(
        commands_patched):
    runner = CliRunner()
    command = "experiments createAndStart multinode " \
              "--name exp1 " \
              "--projectHandle testHandle " \
              "--experimentTypeId MPI " \
              "--workerContainer testWorkerContainer " \
              "--workerMachineType testWorkerMachineType " \
              "--workerCommand testWorkerCommand " \
              "--workerCount 2 " \
              "--parameterServerContainer testParameterServerContainer " \
              "--parameterServerMachineType testParameterServerMachineType " \
              "--parameterServerCommand testParameterServerCommand " \
              "--parameterServerCount 3"
    expected_kwargs = {"name": u"exp1",
                       "projectHandle": u"testHandle",
                       "experimentTypeId": constants.ExperimentType.MPI_MULTI_NODE,
                       "workerContainer": u"testWorkerContainer",
                       "workerMachineType": u"testWorkerMachineType",
                       "workerCommand": u"testWorkerCommand",
                       "workerCount": 2,
                       "parameterServerContainer": u"testParameterServerContainer",
                       "parameterServerMachineType": u"testParameterServerMachineType",
                       "parameterServerCommand": u"testParameterServerCommand",
                       "parameterServerCount": 3,
                       }

    result = runner.invoke(cli.cli, command.split())

    assert result.exit_code == 0
    commands_patched.create_and_start_experiment.assert_called_once_with(expected_kwargs)

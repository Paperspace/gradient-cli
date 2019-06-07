import mock
from click.testing import CliRunner

from gradient import constants
from gradient.cli import cli


@mock.patch("gradient.client.API")
@mock.patch("gradient.commands.experiments.CreateExperimentCommand.execute")
def test_should_execute_create_experiment_command_when_cli_singlenode_command_was_executed(command_patched,
                                                                                           api_patched):
    api_patched.return_value = mock.MagicMock()
    runner = CliRunner()
    command = "experiments create singlenode " \
              "--name exp1 " \
              "--projectId testHandle " \
              "--container testContainer " \
              "--machineType testType " \
              "--command testCommand " \
              "--workspaceUrl wUrl " \
              "--apiKey some_key"
    expected_kwargs = {"name": u"exp1",
                       "projectHandle": u"testHandle",
                       "container": u"testContainer",
                       "machineType": u"testType",
                       "command": u"testCommand",
                       "experimentTypeId": constants.ExperimentType.SINGLE_NODE,
                       "workspaceUrl": "wUrl",
                       }

    result = runner.invoke(cli.cli, command.split())

    assert result.exit_code == 0
    command_patched.assert_called_once_with(expected_kwargs)


@mock.patch("gradient.client.API")
@mock.patch("gradient.commands.experiments.CreateExperimentCommand.execute")
def test_should_execute_create_experiment_command_when_cli_multinode_mpi_command_was_executed(command_patched,
                                                                                              api_patched):
    api_patched.return_value = mock.MagicMock()
    runner = CliRunner()
    command = "experiments create multinode " \
              "--name exp1 " \
              "--projectId testHandle " \
              "--experimentType MPI " \
              "--workerContainer testWorkerContainer " \
              "--workerMachineType testWorkerMachineType " \
              "--workerCommand testWorkerCommand " \
              "--workerCount 2 " \
              "--parameterServerContainer testParameterServerContainer " \
              "--parameterServerMachineType testParameterServerMachineType " \
              "--parameterServerCommand testParameterServerCommand " \
              "--parameterServerCount 3 " \
              "--workspaceUrl wUrl " \
              "--apiKey some_key"
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
                       "workspaceUrl": "wUrl",
                       }

    result = runner.invoke(cli.cli, command.split())

    assert result.exit_code == 0
    command_patched.assert_called_once_with(expected_kwargs)


@mock.patch("gradient.client.API")
@mock.patch("gradient.commands.experiments.CreateExperimentCommand.execute")
def test_should_execute_create_experiment_command_when_cli_multinode_grpc_command_was_executed(command_patched,
                                                                                               api_patched):
    api_patched.return_value = mock.MagicMock()
    runner = CliRunner()
    command = "experiments create multinode " \
              "--name exp1 " \
              "--projectId testHandle " \
              "--experimentType GRPC " \
              "--workerContainer testWorkerContainer " \
              "--workerMachineType testWorkerMachineType " \
              "--workerCommand testWorkerCommand " \
              "--workerCount 2 " \
              "--parameterServerContainer testParameterServerContainer " \
              "--parameterServerMachineType testParameterServerMachineType " \
              "--parameterServerCommand testParameterServerCommand " \
              "--parameterServerCount 3 " \
              "--workspaceUrl wUrl"
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
                       "workspaceUrl": "wUrl",
                       }

    result = runner.invoke(cli.cli, command.split())

    assert result.exit_code == 0
    command_patched.assert_called_once_with(expected_kwargs)


@mock.patch("gradient.client.API")
@mock.patch("gradient.commands.experiments.CreateAndStartExperimentCommand.execute")
def test_should_execute_create_experiment_command_when_cli_create_and_start_singlenode_command_was_executed(
        command_patched, api_patched):
    api_patched.return_value = mock.MagicMock()
    runner = CliRunner()
    command = "experiments run singlenode " \
              "--name exp1 " \
              "--projectId testHandle " \
              "--container testContainer " \
              "--machineType testType " \
              "--command testCommand " \
              "--workspaceUrl wUrl " \
              "--apiKey some_key " \
              "--no-logs"
    expected_kwargs = {"name": u"exp1",
                       "projectHandle": u"testHandle",
                       "container": u"testContainer",
                       "machineType": u"testType",
                       "command": u"testCommand",
                       "experimentTypeId": constants.ExperimentType.SINGLE_NODE,
                       "workspaceUrl": "wUrl",
                       }

    result = runner.invoke(cli.cli, command.split())

    assert result.exit_code == 0
    command_patched.assert_called_once_with(expected_kwargs)


@mock.patch("gradient.client.API")
@mock.patch("gradient.commands.experiments.CreateAndStartExperimentCommand.execute")
def test_should_execute_create_experiment_command_when_cli_create_and_start_multinode_mpi_command_was_executed(
        command_patched, api_patched):
    api_patched.return_value = mock.MagicMock()
    runner = CliRunner()
    command = "experiments run multinode " \
              "--name exp1 " \
              "--projectId testHandle " \
              "--experimentType MPI " \
              "--workerContainer testWorkerContainer " \
              "--workerMachineType testWorkerMachineType " \
              "--workerCommand testWorkerCommand " \
              "--workerCount 2 " \
              "--parameterServerContainer testParameterServerContainer " \
              "--parameterServerMachineType testParameterServerMachineType " \
              "--parameterServerCommand testParameterServerCommand " \
              "--parameterServerCount 3 " \
              "--workspaceUrl wUrl " \
              "--no-logs"
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
                       "workspaceUrl": "wUrl",
                       }

    result = runner.invoke(cli.cli, command.split())

    assert result.exit_code == 0
    command_patched.assert_called_once_with(expected_kwargs)

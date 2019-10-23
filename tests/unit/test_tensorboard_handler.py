import mock
import pytest

from gradient.commands.experiments import TensorboardHandler


@pytest.fixture()
def tensorboard_handler():
    tensorboard_handler = TensorboardHandler("some_key")
    return tensorboard_handler


class TestTensorboardHandler(object):
    def test_should_add_experiment_to_tensorboard_when_tensorboard_is_a_string(self, tensorboard_handler):
        tensorboard_handler._add_experiment_to_tensorboard = mock.MagicMock()
        tensorboard_handler._create_tensorboard_with_experiment = mock.MagicMock()
        tensorboard_handler._get_tensorboards = mock.MagicMock()

        tensorboard_handler.maybe_add_to_tensorboard("some_tensorboard_id", "some_experiment_id")

        tensorboard_handler._add_experiment_to_tensorboard.assert_called_once_with("some_tensorboard_id",
                                                                                   "some_experiment_id")
        tensorboard_handler._create_tensorboard_with_experiment.assert_not_called()
        tensorboard_handler._get_tensorboards.assert_not_called()

    def test_should_add_experiment_to_tensorboard_when_tensorboard_is_not_a_string_and_one_tb_exists(
            self, tensorboard_handler):
        tensorboard_handler._add_experiment_to_tensorboard = mock.MagicMock()
        tensorboard_handler._create_tensorboard_with_experiment = mock.MagicMock()
        fake_tensorboard = mock.Mock()
        fake_tensorboard.id = "some_tensorboard_id"
        tensorboards = [fake_tensorboard]
        tensorboard_handler._get_tensorboards = mock.MagicMock(return_value=tensorboards)

        tensorboard_handler.maybe_add_to_tensorboard(True, "some_experiment_id")

        tensorboard_handler._get_tensorboards.assert_called_once()
        tensorboard_handler._add_experiment_to_tensorboard.assert_called_once_with("some_tensorboard_id",
                                                                                   "some_experiment_id")
        tensorboard_handler._create_tensorboard_with_experiment.assert_not_called()

    def test_should_add_experiment_to_tensorboard_when_tensorboard_is_not_a_string_and_more_than_one_tb_exists(
            self, tensorboard_handler):
        tensorboard_handler._add_experiment_to_tensorboard = mock.MagicMock()
        tensorboard_handler._create_tensorboard_with_experiment = mock.MagicMock()
        fake_tensorboard = mock.Mock()
        fake_tensorboard.id = "some_tensorboard_id"
        tensorboards = [fake_tensorboard, fake_tensorboard]
        tensorboard_handler._get_tensorboards = mock.MagicMock(return_value=tensorboards)

        tensorboard_handler.maybe_add_to_tensorboard(True, "some_experiment_id")

        tensorboard_handler._get_tensorboards.assert_called_once()
        tensorboard_handler._add_experiment_to_tensorboard.assert_not_called()
        tensorboard_handler._create_tensorboard_with_experiment.assert_called_once_with("some_experiment_id")

    def test_should_add_experiment_to_tensorboard_when_tensorboard_is_not_a_string_and_no_tb_exists(
            self, tensorboard_handler):
        tensorboard_handler._add_experiment_to_tensorboard = mock.MagicMock()
        tensorboard_handler._create_tensorboard_with_experiment = mock.MagicMock()
        tensorboards = []
        tensorboard_handler._get_tensorboards = mock.MagicMock(return_value=tensorboards)

        tensorboard_handler.maybe_add_to_tensorboard(True, "some_experiment_id")

        tensorboard_handler._get_tensorboards.assert_called_once()
        tensorboard_handler._add_experiment_to_tensorboard.assert_not_called()
        tensorboard_handler._create_tensorboard_with_experiment.assert_called_once_with("some_experiment_id")

    @mock.patch("gradient.commands.tensorboards.AddExperimentToTensorboard")
    def test_should_execute_proper_command_when__add_experiment_to_tensorboard_was_executed(
            self, command_class_patched, tensorboard_handler):
        command = mock.MagicMock()
        command_class_patched.return_value = command

        tensorboard_handler._add_experiment_to_tensorboard("tensorboard_id", "experiment_id")

        command_class_patched.assert_called_once_with(api_key="some_key")
        command.execute.assert_called_once_with("tensorboard_id", ["experiment_id"])

    @mock.patch("gradient.commands.experiments.TensorboardClient")
    def test_should_execute_proper_command_when__get_tensorboards_was_executed(
            self, client_class_patched, tensorboard_handler):
        client = mock.MagicMock()
        client_class_patched.return_value = client

        tensorboard_handler._get_tensorboards()

        client_class_patched.assert_called_once_with(api_key="some_key", logger=tensorboard_handler.logger)
        client.list.assert_called_once_with()

    @mock.patch("gradient.commands.tensorboards.CreateTensorboardCommand")
    def test_should_execute_proper_command_when__create_tensorboard_with_experiment(
            self, client_class_patched, tensorboard_handler):
        command = mock.MagicMock()
        client_class_patched.return_value = command

        tensorboard_handler._create_tensorboard_with_experiment("experiment_id")

        client_class_patched.assert_called_once_with(api_key=tensorboard_handler.api_key)
        command.execute.assert_called_once_with(experiments=["experiment_id"])

import pytest

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path


@pytest.fixture
def create_single_node_experiment_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "experiments_create_single_node.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def create_multi_node_experiment_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "experiments_create_multi_node.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def experiment_details_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "experiments_details.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def experiments_list_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "experiments_list.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def experiments_start_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "experiments_start.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def experiments_stop_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "experiments_stop.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def experiments_logs_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "experiments_logs.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def deployments_create_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "deployments_create.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def deployments_list_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "deployments_list.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def deployments_start_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "deployments_start.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def deployments_stop_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "deployments_stop.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def hyperparameters_create_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "hyperparameters_create.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def hyperparameters_start_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "hyperparameters_start.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def hyperparameters_list_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "hyperparameters_list.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def hyperparameters_details_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "hyperparameters_details.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def jobs_list_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "jobs_list.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def jobs_logs_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "jobs_logs.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def jobs_artifacts_destroy_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "jobs_artifacts_destroy.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def jobs_artifacts_get_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "jobs_artifacts_get.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def jobs_artifacts_list_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "jobs_artifacts_list.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def jobs_create_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "jobs_create.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def machines_availability_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "machines_availability.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def machines_create_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "machines_create.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def machines_destroy_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "machines_destroy.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def machines_list_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "machines_list.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def machines_restart_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "machines_restart.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def machines_show_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "machines_show.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def machines_start_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "machines_start.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def machines_stop_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "machines_stop.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def machines_update_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "machines_update.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def machines_utilization_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "machines_utilization.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def machines_waitfor_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "machines_waitfor.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def models_list_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "models_list.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def projects_list_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "projects_list.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def projects_create_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "projects_create.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def run_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "run.yaml"
    return str(fixture_dir.resolve())

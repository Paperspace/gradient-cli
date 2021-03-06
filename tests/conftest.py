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
def create_multi_node_experiment_ds_objects_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "experiments_create_multi_node_ds_objs.yaml"
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
def experiments_metrics_get_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "experiments_metrics_get.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def experiments_metrics_stream_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "experiments_metrics_stream.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def deployments_create_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "deployments_create.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def deployments_update_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "deployments_update.yaml"
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
    fixture_dir = p.parent / "config_files" / "deployments_delete.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def deployments_delete_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "deployments_stop.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def deployments_details_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "deployments_details.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def deployments_metrics_get_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "deployments_metrics_get.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def deployments_metrics_stream_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "deployments_metrics_stream.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def deployments_logs_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "deployments_logs.yaml"
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
def jobs_metrics_get_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "jobs_metrics_get.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def jobs_metrics_stream_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "jobs_metrics_stream.yaml"
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
def models_details_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "models_details.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def models_delete_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "models_delete.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def projects_list_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "projects_list.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def projects_details_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "projects_details.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def projects_create_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "projects_create.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def projects_delete_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "projects_delete.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def run_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "run.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def notebooks_create_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "notebooks_create.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def notebooks_delete_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "notebooks_delete.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def notebooks_show_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "notebooks_show.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def notebooks_list_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "notebooks_list.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def notebooks_metrics_get_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "notebooks_metrics_get.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def notebooks_metrics_stream_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "notebooks_metrics_stream.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def tensorboards_create_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "tensorboards_create.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def tensorboards_details_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "tensorboards_details.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def experiments_delete_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "experiments_delete.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def models_upload_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "models_upload.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def entity_tags_add_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "entity_tags_add.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def entity_tags_remove_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "entity_tags_remove.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def clusters_list_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "clusters_list.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def vm_machine_types_list_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "vm_machine_types_list.yaml"
    return str(fixture_dir.resolve())

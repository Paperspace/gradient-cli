import pytest

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path


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

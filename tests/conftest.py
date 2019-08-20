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

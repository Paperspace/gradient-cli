import pytest

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path


@pytest.fixture
def create_single_node_experiment_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "create_single_node_experiment.yaml"
    return str(fixture_dir.resolve())


@pytest.fixture
def create_multi_node_experiment_config_path():
    p = Path(__file__)
    fixture_dir = p.parent / "config_files" / "create_multi_node_experiment.yaml"
    return str(fixture_dir.resolve())

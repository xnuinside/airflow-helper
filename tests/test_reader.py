import pathlib

import pydantic_core
import pytest

from airflow_helper.reader import ConfigReader


@pytest.fixture
def example_config_path():
    base_folder = pathlib.Path(__file__).parents[1]
    return str(base_folder / "example/airflow_settings_local.yaml")


def test_config_reader_file_exists(example_config_path: str):
    reader = ConfigReader(file_path=example_config_path)
    assert reader.config_file


def test_config_reader_file_not_exists():
    with pytest.raises(pydantic_core._pydantic_core.ValidationError) as e:
        ConfigReader(file_path="undefined.yaml")
    assert "Path does not point to a file" in str(e)


def test_config(example_config_path: str):
    reader = ConfigReader(file_path=example_config_path)
    config = reader.load_config()

    assert config.airflow
    assert len(config.airflow.connections) == 2
    assert len(config.airflow.pools) == 2
    assert len(config.airflow.variables) == 3

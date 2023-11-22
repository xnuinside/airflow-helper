import yaml

from airflow_helper.models import Config, ConfigFile
from airflow_helper.settings import settings as s


class ConfigReader:
    def __init__(self, file_path: str = s.config_file_name) -> None:
        self.config_file = ConfigFile(file_path=file_path)
        self.config = None

    @staticmethod
    def _populate_config_data(config_data: dict, added_config: dict) -> None:
        # we adding connections, pools, variables, not overwrite
        for key, value in added_config.get("airflow", {}).items():
            if not config_data["airflow"].get(key):
                config_data["airflow"][key] = []
            config_data["airflow"][key].extend(value)

    def resolve_included_config_path(self, path: str) -> str:
        if "/" not in path:
            path = self.config_file.file_path.parents[0] / path
        return path

    def process_included_configs(self, base_config_data: dict) -> None:
        include_configs = base_config_data.get("include", [])
        config_data = {"airflow": {}}
        for path in include_configs:
            if path.strip():
                included_config_path = self.resolve_included_config_path(path)
                parent_config = self.read_config_yaml(included_config_path)
                if parent_config:
                    self._populate_config_data(config_data, parent_config)
                    if parent_config.get("include"):
                        parent_config_included_data = self.process_included_configs(
                            parent_config
                        )
                        self._populate_config_data(
                            config_data, parent_config_included_data
                        )
        self._populate_config_data(config_data, base_config_data)
        return config_data

    def load_config(self):
        base_config_data = self.read_config_yaml(self.config_file.file_path)
        config_data = self.process_included_configs(base_config_data)
        self.config = Config(**config_data)
        return self.config

    def read_config_yaml(self, file_path: str):
        with open(file_path, "r") as f:
            return yaml.safe_load(f)

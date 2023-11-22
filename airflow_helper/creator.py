import yaml

from airflow_helper.models import EmptyConfig
from airflow_helper.settings import settings as s


class EmptyConfigCreator:
    def __init__(self, file_path: str = s.config_file_name) -> None:
        self.file_path = file_path
        self.config = None

    def create(self):
        with open(self.file_path, "w+") as f:
            yaml.dump(EmptyConfig().model_dump(), f)

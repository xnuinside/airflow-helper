import yaml
from airflow_helper.models import ConfigFile, Config


class ConfigReader:
    
    file: ConfigFile
    
    def __init__(self, file_path: str, not_strict: bool = False) -> None:
        """ if not_strict is setting up, this mean in yaml file can be properties that is not supported by Airflow Helper"""
        self.config_file = ConfigFile(file_path=file_path)
        self.not_strict = not_strict
        self.config = self.read_and_validate_config()
    
    def read_and_validate_config(self):
        config_data = self.load_config_yaml()
        if not self.not_strict:
            print(Config.model_json_schema())

    def load_config_yaml(self):
        with open(self.config_file.path, 'r') as f:
            return yaml.safe_load(f)
    
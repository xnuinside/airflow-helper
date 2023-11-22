import logging

from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__file__)


class Settings(BaseSettings):
    # remote connection settings
    port: int = 8080
    host: str = "http://localhost"
    protocol: str = "http://"
    api_postfix: str = "api/v1"
    # airflow default pass & login
    password: str = "airflow"
    user: str = "airflow"
    # config
    config_file_name: str = "airflow_settings.yaml"
    # upload settings
    overwrite: bool = False

    model_config = SettingsConfigDict(env_prefix="airflow_helper_")


settings = Settings()

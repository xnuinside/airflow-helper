""" method to obtain data from remote Apache Airflow server """

from typing import List

import airflow_client.client
import yaml
from airflow_client.client.api import connection_api, pool_api, variable_api

from airflow_helper.api import AirflowAPIBase
from airflow_helper.models import AirflowConfig, Config, Connection, Pool, Variable
from airflow_helper.settings import logger
from airflow_helper.settings import settings as s


class RemoteConfigObtainter:
    def __init__(self, by_api: bool = True, **kwargs) -> None:
        if by_api:
            self.connector = AirflowAPIGrabber(**kwargs)
        else:
            self.connector = DBGrabber(**kwargs)

    def dump_config(self, file_path: str = s.config_file_name) -> None:
        config = self.connector.collect_full_config()

        logger.info(f"Dumping config to the path {file_path}")

        with open(file_path, "w+") as f:
            yaml.dump(config.model_dump(exclude_unset=True), f)


class DBGrabber:
    def __init__(self):
        raise NotImplementedError(
            "Getting Variables, Connections & Pools directly from Airflow DB will be available in next releases"
        )


class AirflowAPIGrabber(AirflowAPIBase):
    def get_pools(self) -> List[Pool]:
        with airflow_client.client.ApiClient(self.conn_config) as api_client:
            pools = pool_api.PoolApi(api_client).get_pools()["pools"]
            pools_list = []
            for pool in pools:
                pools_list.append(Pool(**pool._data_store))
            return pools_list

    def get_variables(self) -> List[Variable]:
        with airflow_client.client.ApiClient(self.conn_config) as api_client:
            variables = variable_api.VariableApi(api_client).get_variables()[
                "variables"
            ]
            variables_list = []
            for variable in variables:
                variables_list.append(Variable(**variable._data_store))
            return variables_list

    def get_connections(self) -> List[Connection]:
        with airflow_client.client.ApiClient(self.conn_config) as api_client:
            connections = connection_api.ConnectionApi(api_client).get_connections()[
                "connections"
            ]
            connections_list = []
            for connection in connections:
                connections_list.append(Connection(**connection._data_store))
            return connections_list

    def collect_full_config(self) -> AirflowConfig:
        return Config(
            airflow=AirflowConfig(
                variables=self.get_variables(),
                connections=self.get_connections(),
                pools=self.get_pools(),
            )
        )

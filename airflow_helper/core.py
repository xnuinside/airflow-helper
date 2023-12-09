import sys
from typing import Callable, List, Union

import airflow_client
from airflow_client.client.api import connection_api, pool_api, variable_api
from airflow_client.client.api.connection_api import Connection as APIConnection
from airflow_client.client.api.pool_api import Pool as APIPool
from airflow_client.client.api.variable_api import Variable as APIVariable

from airflow_helper.api import AirflowAPIBase
from airflow_helper.models import Connection, Pool, Variable
from airflow_helper.reader import ConfigReader
from airflow_helper.remote import AirflowAPIGrabber
from airflow_helper.settings import logger
from airflow_helper.settings import settings as s


class ConfigUploader:
    def __init__(
        self,
        file_path: str = s.config_file_name,
        overwrite: bool = s.overwrite,
        skip_existed: bool = s.skip_existed,
        **kwargs,
    ) -> None:
        self.api = PostAirflowAPI(
            overwrite=overwrite, skip_existed=skip_existed, **kwargs
        )
        self.config = ConfigReader(file_path=file_path).load_config()

    def upload_config_to_server(self):
        logger.info(f"Uploading connections to airflow server: {self.api.url}")
        if self.config.airflow.connections:
            self.api.create_connections(self.config.airflow.connections)
        if self.config.airflow.pools:
            logger.info(f"Uploading pools to airflow server: {self.api.url}")
            self.api.create_pools(self.config.airflow.pools)
        if self.config.airflow.variables:
            logger.info(f"Uploading variables to airflow server: {self.api.url}")
            self.api.create_variables(self.config.airflow.variables)


class PostAirflowAPI(AirflowAPIBase):
    def __init__(self, overwrite: bool = False, skip_existed: bool = False, **kwargs):
        self.overwrite = overwrite
        self.skip_existed = skip_existed
        self.kwargs = kwargs
        super().__init__(**kwargs)

    def post_items(
        self,
        data: List[Union[Connection, Variable, Pool]],
        api_method: Callable,
        api_model: Union[APIConnection, APIPool, APIVariable],
    ):
        items_to_patch = []
        for item in data:
            try:
                api_method(api_model(**item.model_dump(exclude_none=True)))
            except airflow_client.client.exceptions.ApiException as e:
                if "409" in str(e):
                    # mean we have already duplicate
                    if self.overwrite:
                        items_to_patch.append(item)
                elif self.skip_existed is False:
                    raise e
                else:
                    logger.error(
                        f"Item {item} already exists in Airflow Server. Skipped. \n"
                    )
        return items_to_patch

    def patch_connections(
        self, items_to_patch: List[Pool], api_client: airflow_client.client.ApiClient
    ) -> None:
        for connection in items_to_patch:
            connection_api.ConnectionApi(api_client).patch_connection(
                connection.connection_id,
                APIConnection(**connection.model_dump(exclude_none=True)),
            )

    def filter_existed_connections(self, connections: List[Connection]) -> None:
        if not self.overwrite:
            # get list of variables on server first and filter variables that already exists,
            # because Airflow anyway overwrite variables
            api_get = AirflowAPIGrabber(**self.kwargs)
            connections_on_server = api_get.get_connections()
            connections_on_server = {
                connection.connection_id: connection
                for connection in connections_on_server
            }
            to_post_connections = []
            for connection in connections:
                if (
                    connection.connection_id in connections_on_server
                    and connection.conn_type
                    == connections_on_server[connection.connection_id].conn_type
                ):
                    message = f"""ERROR: Connection with connection_id `{connection.connection_id}`
                    and type `{connection.conn_type}` already exists  \n"""
                    logger.error(message)
                    if not self.skip_existed:
                        sys.exit(1)
                else:
                    to_post_connections.append(connection)
            return to_post_connections
        return connections

    def create_connections(self, connections: List[Connection]) -> None:
        connections = self.filter_existed_connections(connections)

        with airflow_client.client.ApiClient(self.conn_config) as api_client:
            items_to_patch = self.post_items(
                connections,
                connection_api.ConnectionApi(api_client).post_connection,
                APIConnection,
            )
            if self.overwrite and items_to_patch:
                self.patch_connections(items_to_patch, api_client)

    def patch_pools(
        self, items_to_patch: List[Pool], api_client: airflow_client.client.ApiClient
    ) -> None:
        for pool in items_to_patch:
            pool_api.PoolApi(api_client).patch_pool(
                pool.name, APIPool(**pool.model_dump(exclude_none=True))
            )

    def create_pools(self, pools: List[Connection]) -> None:
        with airflow_client.client.ApiClient(self.conn_config) as api_client:
            items_to_patch = self.post_items(
                pools, pool_api.PoolApi(api_client).post_pool, APIPool
            )
            if self.overwrite and items_to_patch:
                self.patch_pools(items_to_patch, api_client)

    def filter_existed_variables(self, variables: List[Variable]) -> None:
        if not self.overwrite:
            # get list of variables on server first and filter variables that already exists,
            # because Airflow anyway overwrite variables
            api_get = AirflowAPIGrabber(**self.kwargs)
            variables_on_server = api_get.get_variables()
            variables_on_server = {variable.key for variable in variables_on_server}
            to_post_variables = []
            for variable in variables:
                if variable.key in variables_on_server:
                    message = (
                        f"ERROR: Variable with name `{variable.key}` already exists \n"
                    )
                    logger.error(message)
                    if not self.skip_existed:
                        sys.exit(1)
                else:
                    to_post_variables.append(variable)
            return to_post_variables
        return variables

    def create_variables(self, variables: List[Variable]) -> None:
        variables = self.filter_existed_variables(variables)

        with airflow_client.client.ApiClient(self.conn_config) as api_client:
            self.post_items(
                variables,
                variable_api.VariableApi(api_client).post_variables,
                APIVariable,
            )

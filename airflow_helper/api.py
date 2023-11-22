from typing import Optional

import airflow_client.client
from pydantic import validate_call

from airflow_helper.settings import logger
from airflow_helper.settings import settings as s


class AirflowAPIBase:
    @validate_call
    def __init__(
        self,
        user: Optional[str] = None,
        password: Optional[str] = None,
        url: Optional[str] = None,
        port: Optional[int] = None,
        host: Optional[str] = None,
    ) -> None:
        self.url = self.get_airflow_url(url=url, port=port, host=host)
        self.conn_config = airflow_client.client.Configuration(
            host=self.url,
            username=user or s.user,
            password=password or s.password,
        )

    @staticmethod
    def get_airflow_url(
        url: Optional[str] = None,
        port: Optional[int] = None,
        host: Optional[str] = None,
    ):
        if url:
            logger.info(f"Provided full url to Airflow Server, will be used: {url}")
            if url.endswith("/"):
                url = url[:-1]
        else:
            if not port:
                logger.info(f"Port is not provided. Will be used default: {s.port}")
                port = s.port
            if not host:
                logger.info(f"Host is not provided. Will be used default: {s.host}")
                host = s.host
            url = f"{host}:{port}"
        if "://" not in url:
            logger.info(
                f"Protocol is not provided in the host url. Will be used default: {s.protocol}"
            )
            url = f"{s.protocol}{url}"
        return f"{url}/{s.api_postfix}"

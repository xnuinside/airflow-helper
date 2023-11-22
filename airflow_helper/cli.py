from typing import Optional

import typer
from typing_extensions import Annotated

from airflow_helper import ConfigUploader, EmptyConfigCreator, RemoteConfigObtainter
from airflow_helper.settings import settings as s

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


main_app = typer.Typer(context_settings=CONTEXT_SETTINGS)

create_app = typer.Typer()
server_args = []


@create_app.command(help="Create new empty config")
def new(
    file_path: Annotated[
        Optional[str], typer.Argument(..., help="File path there to store config.")
    ] = s.config_file_name,
):
    EmptyConfigCreator(file_path=file_path).create()


@create_app.command(help="Create config with values from existed Airflow Server")
def from_server(
    file_path: Annotated[
        Optional[str], typer.Argument(..., help="File path where to store config.")
    ] = s.config_file_name,
    url: Annotated[
        str,
        typer.Option(
            help="Apache Airflow full url to connect. You can provide it or host & port separately."
        ),
    ] = None,
    host: Annotated[
        str,
        typer.Option(
            help="Apache Airflow server host form that obtain existed settings"
        ),
    ] = s.host,
    port: Annotated[
        str,
        typer.Option(
            help="Apache Airflow server port form that obtain existed settings"
        ),
    ] = s.port,
    user: Annotated[
        str, typer.Option("--user", "-u", help="Apache Airflow user with read rights")
    ] = s.user,
    password: Annotated[
        str, typer.Option("--password", "-p", help="Apache Airflow user password")
    ] = s.password,
):
    RemoteConfigObtainter(
        user=user, password=password, url=url, host=host, port=port
    ).dump_config(file_path=file_path)


@main_app.command(help="Load settings from yaml config to the Apache Airflow server")
def load(
    file_path: Annotated[
        Optional[str], typer.Argument(..., help="File path to config.")
    ] = s.config_file_name,
    url: Annotated[
        str,
        typer.Option(
            help="Apache Airflow full url to connect. You can provide it or host & port separately."
        ),
    ] = None,
    host: Annotated[
        str,
        typer.Option(
            help="Apache Airflow server host form that obtain existed settings"
        ),
    ] = s.host,
    port: Annotated[
        str,
        typer.Option(
            help="Apache Airflow server port form that obtain existed settings"
        ),
    ] = s.port,
    user: Annotated[
        str, typer.Option("--user", "-u", help="Apache Airflow user with read rights")
    ] = s.user,
    password: Annotated[
        str, typer.Option("--password", "-p", help="Apache Airflow user password")
    ] = s.password,
):
    ConfigUploader(
        file_path=file_path, url=url, host=host, port=port, user=user, password=password
    ).upload_config_to_server()


main_app.add_typer(
    create_app,
    name="create",
    help="Create new airflow settings config - from existed server or empty",
)


def cli():
    main_app()

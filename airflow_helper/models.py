from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, FilePath, constr


class ConfigFile(BaseModel):
    file_path: FilePath


class EmptyConnection(BaseModel):
    connection_id: str = Field(alias="id", default="")
    conn_type: str = Field(alias="type", default="")
    host: Optional[str] = ""
    login: Optional[str] = ""
    password: Optional[str] = ""
    port: Optional[int] = 5000
    extra: Optional[str] = ""

    model_config = ConfigDict(
        populate_by_name=True,
    )


class Connection(EmptyConnection):
    connection_id: constr(min_length=1) = Field(alias="id")
    conn_type: str = Field(alias="type")
    host: Optional[str] = None
    login: Optional[str] = None
    password: Optional[str] = None
    port: Optional[int] = None
    extra: Optional[str] = None


class EmptyPool(BaseModel):
    name: Optional[str] = ""
    slots: Optional[int] = 120
    description: Optional[str] = ""
    include_deferred: bool = False


class Pool(EmptyPool):
    name: constr(min_length=1)
    slots: int
    description: Optional[str] = None


class EmptyVariable(BaseModel):
    key: Optional[str] = ""
    value: Optional[str] = ""
    description: Optional[str] = ""


class Variable(EmptyVariable):
    key: constr(min_length=1)
    value: str


class AirflowConfig(BaseModel):
    connections: Optional[List[Connection]] = None
    pools: Optional[List[Pool]] = None
    variables: Optional[List[Variable]] = None


class EmptyAirflowConfig(BaseModel):
    connections: List[EmptyConnection] = [EmptyConnection()]
    pools: List[EmptyPool] = [EmptyPool()]
    variables: List[EmptyVariable] = [EmptyVariable()]


class EmptyConfig(BaseModel):
    include: List[str] = [""]
    project_name: Optional[str] = ""
    airflow: EmptyAirflowConfig = EmptyAirflowConfig()


class Config(EmptyConfig):
    airflow: AirflowConfig

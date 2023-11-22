from pydantic import BaseModel, FilePath
from typing import List


class ConfigFile(BaseModel):
    file_path: FilePath


class Connection(BaseModel):
    
    id: str
    type: str
    host: str
    login: str
    password: str
    port: int
    extra: dict

    
class AirflowConfig(BaseModel):
    
    connections: Connection
 
   
class Config(BaseModel):
    """ allowed config fields """
    include: List[str]
    airflow: AirflowConfig
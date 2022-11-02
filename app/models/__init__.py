from enum import Enum
from typing import Any, List, Optional

from pydantic import BaseModel
from pydantic.dataclasses import dataclass


class SchemaEntityConfig:
    extra = "forbid"


@dataclass(config=SchemaEntityConfig)
class EpigraphdbNodeEntity:
    "Pydantic basemodel for an epigraphdb node"


@dataclass(config=SchemaEntityConfig)
class EpigraphdbRelEntity:
    "Pydantic basemodel for an epigraphdb rel"

    class _Path:
        source: str
        target: str


class EpigraphdbGraphs(str, Enum):
    epigraphdb = "epigraphdb"
    pqtl = "pqtl"


class EpigraphdbGraphsExtended(str, Enum):
    epigraphdb = "epigraphdb"
    pqtl = "pqtl"
    custom = "custom"


class ApiMetadata(BaseModel):
    query: Optional[str]
    total_seconds: Optional[float]
    empty_results: bool


class ApiGenericResponse(BaseModel):

    metadata: ApiMetadata
    results: List[Any]


class EpigraphdbBuilds(BaseModel):
    overall: str
    database: str
    api: str
    web_app: Optional[str]


class ApiInfoBuilds(BaseModel):
    epigraphdb: EpigraphdbBuilds
    pqtl: str

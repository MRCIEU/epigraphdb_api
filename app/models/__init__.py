from enum import Enum
from typing import Any, List, Optional

from pydantic import BaseModel


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

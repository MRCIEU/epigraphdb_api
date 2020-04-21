from typing import Any, List

from pydantic import BaseModel

from app.models import ApiMetadata


class RawCypherResponse(BaseModel):
    """Response from GET /raw_cypher/"""

    metadata: ApiMetadata
    results: List[Any]

from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from app.models import ApiMetadata


class PQTLResponse(BaseModel):
    metadata: ApiMetadata
    results: List[Dict[str, Any]]


class PQTLPleioProteinsResultsItem(BaseModel):
    expID: str


class PQTLPleioProteinsResponse(BaseModel):
    """/pqtl/pleio/, when prflag == "proteins" """

    metadata: ApiMetadata
    results: List[PQTLPleioProteinsResultsItem]


class PQTLPleioCountResponse(BaseModel):
    """/pqtl/pleio/, when prflag == "count" """

    metadata: Optional[ApiMetadata]
    results: int


class ListPQTLResponse(BaseModel):
    metadata: ApiMetadata
    results: List[Dict[str, str]]

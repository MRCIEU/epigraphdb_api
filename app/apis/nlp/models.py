from typing import List

from pydantic import BaseModel

from app.models import ApiMetadata


class NlpQueryItem(BaseModel):
    id: str
    name: str
    text: str
    score: float
    meta_node: str


class NlpQueryTextResults(BaseModel):
    clean_text: str
    results: List[NlpQueryItem]


class NlpQueryTextResponse(BaseModel):
    metadata: ApiMetadata
    results: NlpQueryTextResults


class NlpQueryEntityResponse(BaseModel):
    metadata: ApiMetadata
    results: List[NlpQueryItem]


class NlpQueryEntityEncodeResponse(BaseModel):
    metadata: ApiMetadata
    results: List[float]

from typing import List

from pydantic import BaseModel

from app.models import ApiMetadata


class ListNamesResultItem(BaseModel):

    name: str


class ListNamesResponse(BaseModel):

    metadata: ApiMetadata
    results: List[ListNamesResultItem]

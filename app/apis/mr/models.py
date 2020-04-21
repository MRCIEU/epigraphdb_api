from typing import List

from pydantic import BaseModel

from app.models import ApiMetadata
from app.models.output_nodes import TraitItem
from app.models.output_rels import MRItem


class MRResultItem(BaseModel):
    exposure: TraitItem
    outcome: TraitItem
    mr: MRItem


class MRResponse(BaseModel):

    metadata: ApiMetadata
    results: List[MRResultItem]

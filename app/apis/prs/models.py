from typing import List

from pydantic import BaseModel

from app.models import ApiMetadata
from app.models.output_nodes import TraitItem
from app.models.output_rels import PrsItem


class PrsResultItem(BaseModel):

    trait: TraitItem
    assoc_trait: TraitItem
    prs: PrsItem


class PrsResponse(BaseModel):

    metadata: ApiMetadata
    results: List[PrsResultItem]

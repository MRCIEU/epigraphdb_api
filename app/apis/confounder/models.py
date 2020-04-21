from typing import List

from pydantic import BaseModel

from app.models import ApiMetadata
from app.models.output_nodes import TraitItem
from app.models.output_rels import MRItem


class ConfounderItem(BaseModel):

    exposure: TraitItem
    outcome: TraitItem
    cf: TraitItem
    r1: MRItem
    r2: MRItem
    r3: MRItem


class ConfounderResponse(BaseModel):

    metadata: ApiMetadata
    results: List[ConfounderItem]

from typing import List

from pydantic import BaseModel

from app.models import ApiMetadata
from app.models.output_nodes import TraitItem
from app.models.output_rels import ObsCorItem


class ObsCorResultItem(BaseModel):

    trait: TraitItem
    assoc_trait: TraitItem
    obs_cor: ObsCorItem


class ObsCorResponse(BaseModel):

    metadata: ApiMetadata
    results: List[ObsCorResultItem]

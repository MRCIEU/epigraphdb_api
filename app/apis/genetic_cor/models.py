from typing import List

from pydantic import BaseModel

from app.models import ApiMetadata
from app.models.output_nodes import TraitItem
from app.models.output_rels import GeneticCorItem


class GeneticCorResultItem(BaseModel):

    trait: TraitItem
    assoc_trait: TraitItem
    gc: GeneticCorItem


class GeneticCorResponse(BaseModel):

    metadata: ApiMetadata
    results: List[GeneticCorResultItem]

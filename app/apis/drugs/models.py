from typing import List

from pydantic import BaseModel

from app.models import ApiMetadata
from app.models.output_nodes import DrugItem, GeneItem, TraitItem, VariantItem
from app.models.output_rels import MRItem


class RiskFactorsResultItem(BaseModel):

    trait: TraitItem
    assoc_trait: TraitItem
    variant: VariantItem
    gene: GeneItem
    drug: DrugItem
    mr: MRItem


class RiskFactorsResponse(BaseModel):

    metadata: ApiMetadata
    results: List[RiskFactorsResultItem]

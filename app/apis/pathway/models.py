from typing import List

from pydantic import BaseModel

from app.models import ApiMetadata
from app.models.output_nodes import (
    GeneItem,
    PathwayItem,
    ProteinItem,
    TraitItem,
    VariantItem,
)
from app.models.output_rels import GwasToVariantItem


class PathwayResultItem(BaseModel):

    gwas: TraitItem
    gwas_to_variant: GwasToVariantItem
    variant: VariantItem
    gene: GeneItem
    protein: ProteinItem
    pathway: PathwayItem


class PathwayResponse(BaseModel):

    metadata: ApiMetadata
    results: List[PathwayResultItem]

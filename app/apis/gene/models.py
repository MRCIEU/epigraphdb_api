from typing import List, Union

from pydantic import BaseModel

from app.models import ApiMetadata
from app.models.output_nodes import DrugItem, GeneItem, ProteinItem
from app.models.output_rels import CpicItem, OpentargetsDrugToTargetItem


class DruggableGeneItem(BaseModel):

    name: str
    druggability_tier: str


class GeneSemmedTripleItem(BaseModel):
    predicate: str
    object_name: str


class GeneDrugsResultItem(BaseModel):

    gene: GeneItem
    drug: DrugItem
    r: Union[OpentargetsDrugToTargetItem, CpicItem]
    r_source: str


class GeneDrugPpiItem(BaseModel):

    g1: GeneItem
    p1: ProteinItem
    p2: ProteinItem
    g2: DruggableGeneItem


class GeneLiteratureItem(BaseModel):

    gene: GeneItem
    pubmed_id: List[str]
    st: GeneSemmedTripleItem


class GeneDrugPpiResponse(BaseModel):

    metadata: ApiMetadata
    results: List[GeneDrugPpiItem]


class GeneLiteratureResponse(BaseModel):

    metadata: ApiMetadata
    results: List[GeneLiteratureItem]


class GeneDrugsResponse(BaseModel):

    metadata: ApiMetadata
    results: List[GeneDrugsResultItem]

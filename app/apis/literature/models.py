from typing import List

from pydantic import BaseModel

from app.models import ApiMetadata
from app.models.output_nodes import (
    LiteratureItem,
    LiteratureTermItem,
    LiteratureTripleItem,
    TraitItem,
)


class OverlappingTermItem(BaseModel):
    name: str
    type: List[str]


class SubjectTripleItem(BaseModel):
    id: str
    subject_id: str
    object_id: str
    predicate: str


class ObjectTripleItem(BaseModel):
    id: str
    subject_id: str
    object_id: str
    predicate: str


class GwasLiteratureTripleItem(BaseModel):
    pval: float
    localCount: int


class LiteratureGwasPairwiseItem(BaseModel):
    gwas: TraitItem
    gs1: GwasLiteratureTripleItem
    st1: LiteratureTermItem
    s1: SubjectTripleItem
    st: OverlappingTermItem
    s2: ObjectTripleItem
    st2: LiteratureTermItem
    assoc_gwas: TraitItem


class LiteratureGwasItem(BaseModel):
    gwas: TraitItem
    gs: GwasLiteratureTripleItem
    triple: LiteratureTripleItem
    lit: LiteratureItem


class LiteratureGwasResponse(BaseModel):
    metadata: ApiMetadata
    results: List[LiteratureGwasItem]


class LiteratureGwasPairwiseResponse(BaseModel):
    metadata: ApiMetadata
    results: List[LiteratureGwasPairwiseItem]

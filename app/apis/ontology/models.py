from typing import List

from pydantic import BaseModel

from app.models import ApiMetadata
from app.models.output_nodes import DiseaseItem, OntologyItem, TraitItem


class GwasNlpEfoItem(BaseModel):
    score: float


class OntologyGwasEfoItem(BaseModel):
    gwas: TraitItem
    r: GwasNlpEfoItem
    efo: OntologyItem


class OntologyDiseaseEfoItem(BaseModel):
    disease: DiseaseItem
    efo: OntologyItem


class OntologyGwasEfoDiseaseItem(BaseModel):
    gwas: TraitItem
    ge: GwasNlpEfoItem
    efo: OntologyItem
    disease: DiseaseItem


class OntologyGwasEfoResponse(BaseModel):
    metadata: ApiMetadata
    results: List[OntologyGwasEfoItem]


class OntologyDiseaseEfoResponse(BaseModel):
    metadata: ApiMetadata
    results: List[OntologyDiseaseEfoItem]


class OntologyGwasEfoDiseaseResponse(BaseModel):
    metadata: ApiMetadata
    results: List[OntologyGwasEfoDiseaseItem]

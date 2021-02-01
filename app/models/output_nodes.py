from pydantic import BaseModel


class TraitItem(BaseModel):
    id: str
    trait: str


class VariantItem(BaseModel):
    name: str


class DrugItem(BaseModel):
    label: str


class GeneItem(BaseModel):
    name: str


class LiteratureItem(BaseModel):
    pubmed_id: str


class ProteinItem(BaseModel):
    uniprot_id: str


class PathwayItem(BaseModel):
    id: str
    name: str

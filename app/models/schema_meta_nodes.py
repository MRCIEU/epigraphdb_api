from typing import List, Optional

from pydantic.dataclasses import dataclass

from app.utils.schema import EpigraphdbNodeEntity


@dataclass
class Disease(EpigraphdbNodeEntity):

    definition: str
    id: str
    label: str
    doid: Optional[List[str]] = None
    efo: Optional[List[str]] = None
    icd10: Optional[List[str]] = None
    icd9: Optional[List[str]] = None
    mesh: Optional[List[str]] = None
    umls: Optional[List[str]] = None

    class Meta:
        _id = "id"
        _name = "label"


@dataclass
class Drug(EpigraphdbNodeEntity):

    label: str
    chembl_uri: Optional[str] = None
    molecule_type: Optional[str] = None

    class Meta:
        _id = "label"
        _name = "label"


@dataclass
class Efo(EpigraphdbNodeEntity):

    id: str
    type: str
    value: str

    class Meta:
        _id = "id"
        _name = "value"


@dataclass
class Gene(EpigraphdbNodeEntity):

    ensembl_id: str
    name: str
    adme_gene: Optional[str] = None
    bio_druggable: Optional[str] = None
    biomart_source: Optional[str] = None
    chr: Optional[str] = None
    description: Optional[str] = None
    druggability_tier: Optional[str] = None
    end: Optional[int] = None
    reactome_id: Optional[str] = None
    small_mol_druggable: Optional[str] = None
    source: Optional[str] = None
    start: Optional[int] = None
    type: Optional[str] = None

    class Meta:
        _id = "ensembl_id"
        _name = "name"


@dataclass
class Gwas(EpigraphdbNodeEntity):

    id: str
    nsnp: str
    trait: str
    author: Optional[str] = None
    build: Optional[str] = None
    category: Optional[str] = None
    consortium: Optional[str] = None
    covariates: Optional[str] = None
    mr: Optional[str] = None
    ncase: Optional[str] = None
    ncontrol: Optional[str] = None
    note: Optional[str] = None
    pmid: Optional[str] = None
    population: Optional[str] = None
    sample_size: Optional[str] = None
    priority: Optional[str] = None
    sd: Optional[str] = None
    sex: Optional[str] = None
    subcategory: Optional[str] = None
    unit: Optional[str] = None
    year: Optional[str] = None

    class Meta:
        _id = "id"
        _name = "trait"


@dataclass
class Literature(EpigraphdbNodeEntity):

    id: str
    doi: Optional[str] = None
    dp: Optional[str] = None
    edat: Optional[str] = None
    issn: Optional[str] = None
    title: Optional[str] = None
    year: Optional[int] = None

    class Meta:
        _id = "id"
        _name = "id"


@dataclass
class LiteratureTerm(EpigraphdbNodeEntity):

    id: str
    name: str
    type: List[str]

    class Meta:
        _id = "id"
        _name = "name"


@dataclass
class LiteratureTriple(EpigraphdbNodeEntity):

    id: str
    name: str
    object_id: str
    predicate: str
    subject_id: str

    class Meta:
        _id = "id"
        _name = "name"


@dataclass
class Pathway(EpigraphdbNodeEntity):

    id: str
    name: str
    url: Optional[str] = None

    class Meta:
        _id = "id"
        _name = "name"


@dataclass
class Protein(EpigraphdbNodeEntity):

    uniprot_id: str
    name: str

    class Meta:
        _id = "uniprot_id"
        _name = "uniprot_id"


@dataclass
class Tissue(EpigraphdbNodeEntity):

    id: str
    name: str

    class Meta:
        _id = "id"
        _name = "name"


# FIXME: meta
# class Meta(EpigraphdbNodeEntity):

#     build_date: Any
#     graph_version: str


@dataclass
class Variant(EpigraphdbNodeEntity):

    name: str
    pos: Optional[int] = None
    chr: Optional[str] = None
    ref: Optional[str] = None
    alt: Optional[str] = None
    build: Optional[str] = None

    class Meta:
        _id = "name"
        _name = "name"


meta_node_schema = {
    "Disease": Disease,
    "Drug": Drug,
    "Efo": Efo,
    "Gene": Gene,
    "Gwas": Gwas,
    "Literature": Literature,
    "LiteratureTerm": LiteratureTerm,
    "LiteratureTriple": LiteratureTriple,
    # FIXME: meta
    # "Meta": Meta,
    "Pathway": Pathway,
    "Protein": Protein,
    "Tissue": Tissue,
    "Variant": Variant,
}

meta_node_id_name_mappings = {
    key: {"id": value.Meta._id, "name": value.Meta._name}  # type: ignore
    for key, value in meta_node_schema.items()
}

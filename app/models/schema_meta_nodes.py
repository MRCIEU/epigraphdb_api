from typing import Any, List, Optional, Union

from app.utils.schema import Neo4jEntity


class Drug(Neo4jEntity):
    """Drug data from Open Targets.
    """

    label: str
    molecule_type: Optional[str]
    chembl_uri: Optional[str]
    source: Union[str, List[str]]


class Efo(Neo4jEntity):
    """Experimental Factor Ontology.
    """

    id: str
    value: str
    type: str


class Event(Neo4jEntity):
    name: str
    in_disease: str
    reactome_id: str


class Gene(Neo4jEntity):
    """Gene data from BioMart (build 37).

    Gene druggability data comes from Finan et al (2017).
    """

    chr: Optional[str]
    type: Optional[str]
    name: Optional[str]
    source: Optional[str]
    ensembl_id: str
    start: Optional[int]
    end: Optional[int]
    description: Optional[str]
    reactome_id: Optional[str]
    adme_gene: Optional[str]
    small_mol_druggable: Optional[str]
    bio_druggable: Optional[str]
    druggability_tier: Optional[str]


class Tissue(Neo4jEntity):
    """Tissue specific gene expression from GTEx.
    """

    tissue: str


class Gwas(Neo4jEntity):
    """GWAS metadata from IEU GWAS Database.
    """

    note: Optional[str]
    access: str
    mr: Optional[str]
    year: Optional[str]
    author: Optional[str]
    consortium: Optional[str]
    sex: Optional[str]
    pmid: Optional[str]
    priority: Optional[str]
    population: Optional[str]
    unit: Optional[str]
    nsnp: str
    sample_size: Optional[str]
    trait: str
    id: str
    category: Optional[str]
    subcategory: Optional[str]
    ncase: Optional[str]
    ncontrol: Optional[str]
    sd: Optional[str]


class Literature(Neo4jEntity):
    """PubMed literature data as available from SemMedDB.
    """

    pubmed_id: str
    issn: str
    dp: str
    year: int
    edat: str


class Meta(Neo4jEntity):
    """Metadata information of EpiGraphDB Graph.
    """

    build_date: Any
    graph_version: str


class Pathway(Neo4jEntity):
    """Biological pathway data from Reactome.
    """

    name: str
    in_disease: str
    reactome_id: str


class Protein(Neo4jEntity):
    """Protein data from BioMart web service (build 37).
    """

    uniprot_id: str


class Disease(Neo4jEntity):
    """Disease data from Mondo Disease Ontology.
    """

    id: str
    label: str
    definition: str
    doid: Optional[List[str]]
    umls: Optional[List[str]]
    efo: Optional[List[str]]
    icd9: Optional[List[str]]
    icd10: Optional[List[str]]
    mesh: Optional[List[str]]


class SemmedTriple(Neo4jEntity):
    id: str
    predicate: str
    subject_name: str
    subject_type: str
    subject_id: str
    object_name: str
    object_type: str
    object_id: str
    count: int


class SemmedTerm(Neo4jEntity):
    name: str
    count: int
    id: str
    type: str


class Variant(Neo4jEntity):
    """SNPs from the following sources:

    - IEU GWAS Database
    - MR-EvE
    - xQTL
    """

    name: str


meta_node_schema = {
    "Disease": Disease,
    "Drug": Drug,
    "Efo": Efo,
    "Event": Event,
    "Gene": Gene,
    "Tissue": Tissue,
    "Gwas": Gwas,
    "Literature": Literature,
    "Meta": Meta,
    "Pathway": Pathway,
    "Protein": Protein,
    "SemmedTerm": SemmedTerm,
    "SemmedTriple": SemmedTriple,
    "Variant": Variant,
}

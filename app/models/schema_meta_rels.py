from typing import Optional

from pydantic.dataclasses import dataclass

from app.utils.schema import EpigraphdbRelEntity


@dataclass
class BIORXIV_OBJ(EpigraphdbRelEntity):
    class _Path:
        source = "LiteratureTriple"
        target = "LiteratureTerm"


@dataclass
class BIORXIV_PREDICATE(EpigraphdbRelEntity):

    count: int
    predicate: str

    class _Path:
        source = "LiteratureTerm"
        target = "LiteratureTerm"


@dataclass
class BIORXIV_SUB(EpigraphdbRelEntity):
    class _Path:
        source = "LiteratureTriple"
        target = "LiteratureTerm"


@dataclass
class BIORXIV_TO_LIT(EpigraphdbRelEntity):
    class _Path:
        source = "LiteratureTriple"
        target = "Literature"


@dataclass
class GEN_COR(EpigraphdbRelEntity):

    rg: float
    p: float
    h2: Optional[float] = None
    h2_SE: Optional[float] = None
    h2_intercept: Optional[float] = None
    h2_intercept_SE: Optional[float] = None
    rpheno: Optional[float] = None
    rg_SE: Optional[float] = None
    Z: Optional[float] = None
    rg_intercept: Optional[float] = None
    rg_intercept_SE: Optional[float] = None

    class _Path:
        source = "Gwas"
        target = "Gwas"


@dataclass
class CPIC(EpigraphdbRelEntity):

    cpic_level: str
    guideline: str
    pgx_on_fda_label: str
    pharmgkb_level_of_evidence: str

    class _Path:
        source = "Drug"
        target = "Gene"


@dataclass
class EFO_CHILD_OF(EpigraphdbRelEntity):
    class _Path:
        source = "Efo"
        target = "Efo"


@dataclass
class EXPRESSED_IN(EpigraphdbRelEntity):

    tpm: float

    class _Path:
        source = "Gene"
        target = "Tissue"


@dataclass
class GENE_TO_PROTEIN(EpigraphdbRelEntity):
    class _Path:
        source = "Gene"
        target = "Protein"


@dataclass
class GWAS_EFO_EBI(EpigraphdbRelEntity):
    class _Path:
        source = "Gwas"
        target = "Efo"


@dataclass
class GWAS_NLP(EpigraphdbRelEntity):

    score: float

    class _Path:
        source = "Gwas"
        target = "Gwas"


@dataclass
class GWAS_NLP_EFO(EpigraphdbRelEntity):

    score: float

    class _Path:
        source = "Gwas"
        target = "Efo"


@dataclass
class GWAS_TO_LITERATURE_TRIPLE(EpigraphdbRelEntity):

    globalCount: int
    globalTotal: int
    localCount: int
    localTotal: int
    odds: float
    pval: float

    class _Path:
        source = "Gwas"
        target = "LiteratureTriple"


@dataclass
class GWAS_TO_LITERATURE(EpigraphdbRelEntity):
    class _Path:
        source = "Gwas"
        target = "Literature"


@dataclass
class GWAS_TO_VARIANT(EpigraphdbRelEntity):

    beta: float
    pval: float
    samplesize: float
    eaf: Optional[float] = None
    ncase: Optional[int] = None
    ncontrol: Optional[int] = None
    se: Optional[float] = None

    class _Path:
        source = "Gwas"
        target = "Variant"


@dataclass
class MEDRXIV_OBJ(EpigraphdbRelEntity):
    class _Path:
        source = "LiteratureTriple"
        target = "LiteratureTerm"


@dataclass
class MEDRXIV_PREDICATE(EpigraphdbRelEntity):

    count: int
    predicate: str

    class _Path:
        source = "LiteratureTerm"
        target = "LiteratureTerm"


@dataclass
class MEDRXIV_SUB(EpigraphdbRelEntity):
    class _Path:
        source = "LiteratureTriple"
        target = "LiteratureTerm"


@dataclass
class MEDRXIV_TO_LIT(EpigraphdbRelEntity):
    class _Path:
        source = "LiteratureTriple"
        target = "Literature"


@dataclass
class METAMAP_LITE(EpigraphdbRelEntity):

    mmi_score: float
    mesh: Optional[str] = None

    class _Path:
        source = "Gwas"
        target = "LiteratureTerm"


@dataclass
class MONDO_MAP_EFO(EpigraphdbRelEntity):
    class _Path:
        source = "Disease"
        target = "Efo"


@dataclass
class MONDO_MAP_UMLS(EpigraphdbRelEntity):
    class _Path:
        source = "Disease"
        target = "LiteratureTerm"


@dataclass
class MR_EVE_MR(EpigraphdbRelEntity):

    b: float
    method: str
    moescore: float
    nsnp: float
    selection: str
    ci_low: Optional[float] = None
    ci_upp: Optional[float] = None
    pval: Optional[float] = None
    se: Optional[float] = None

    class _Path:
        source = "Gwas"
        target = "Gwas"


@dataclass
class OBS_COR(EpigraphdbRelEntity):

    cor: float

    class _Path:
        source = "Gwas"
        target = "Gwas"


@dataclass
class OPENTARGETS_DRUG_TO_DISEASE(EpigraphdbRelEntity):
    class _Path:
        source = "Drug"
        target = "Disease"


@dataclass
class OPENTARGETS_DRUG_TO_TARGET(EpigraphdbRelEntity):

    phase: str
    action_type: str

    class _Path:
        source = "Drug"
        target = "Gene"


@dataclass
class PATHWAY_CHILD_OF(EpigraphdbRelEntity):
    class _Path:
        source = "Pathway"
        target = "Pathway"


@dataclass
class PROTEIN_IN_PATHWAY(EpigraphdbRelEntity):
    class _Path:
        source = "Protein"
        target = "Pathway"


@dataclass
class PRS(EpigraphdbRelEntity):

    beta: float
    model: str
    n: int
    nsnps: int
    p: float
    r2: float
    se: float

    class _Path:
        source = "Gwas"
        target = "Gwas"


@dataclass
class TERM_TO_GENE(EpigraphdbRelEntity):
    class _Path:
        source = "LiteratureTerm"
        target = "Gene"


@dataclass
class SEMMEDDB_OBJ(EpigraphdbRelEntity):
    class _Path:
        source = "LiteratureTriple"
        target = "LiteratureTerm"


@dataclass
class SEMMEDDB_PREDICATE(EpigraphdbRelEntity):

    predicate: str
    count: int

    class _Path:
        source = "LiteratureTerm"
        target = "LiteratureTerm"


@dataclass
class SEMMEDDB_SUB(EpigraphdbRelEntity):
    class _Path:
        source = "LiteratureTriple"
        target = "LiteratureTerm"


@dataclass
class SEMMEDDB_TO_LIT(EpigraphdbRelEntity):
    class _Path:
        source = "LiteratureTriple"
        target = "Literature"


@dataclass
class STRING_INTERACT_WITH(EpigraphdbRelEntity):

    score: float

    class _Path:
        source = "Protein"
        target = "Protein"


@dataclass
class OPENGWAS_TOPHITS(EpigraphdbRelEntity):

    beta: float
    pval: float

    class _Path:
        source = "Gwas"
        target = "Variant"


@dataclass
class VARIANT_TO_GENE(EpigraphdbRelEntity):

    location: str
    allele: str
    feature: str
    feature_type: str
    consequence: str
    cdna_position: str
    cds_position: str
    protein_position: str
    amino_acids: str
    codons: str
    existing_variation: str
    extra: str

    class _Path:
        source = "Variant"
        target = "Gene"


@dataclass
class XQTL_MULTI_SNP_MR(EpigraphdbRelEntity):

    beta: float
    se: float
    p: float
    qtl_type: str
    mr_method: str

    class _Path:
        source = "Gene"
        target = "Gwas"


@dataclass
class XQTL_SINGLE_SNP_MR_GENE_GWAS(EpigraphdbRelEntity):

    beta: float
    se: float
    p: float
    rsid: str
    qtl_type: str

    class _Path:
        source = "Gene"
        target = "Gwas"


@dataclass
class XQTL_SINGLE_SNP_MR_SNP_GENE(EpigraphdbRelEntity):
    class _Path:
        source = "Variant"
        target = "Gene"


@dataclass
class GENE_TO_DISEASE(EpigraphdbRelEntity):

    gene_relationship_type: str
    last_updated: Optional[str] = None

    class _Path:
        source = "Gene"
        target = "Disease"


meta_rel_schema = {
    "BIORXIV_OBJ": BIORXIV_OBJ,
    "BIORXIV_PREDICATE": BIORXIV_PREDICATE,
    "BIORXIV_SUB": BIORXIV_SUB,
    "BIORXIV_TO_LIT": BIORXIV_TO_LIT,
    "CPIC": CPIC,
    "EFO_CHILD_OF": EFO_CHILD_OF,
    "EXPRESSED_IN": EXPRESSED_IN,
    "GENE_TO_PROTEIN": GENE_TO_PROTEIN,
    "GEN_COR": GEN_COR,
    "GWAS_EFO_EBI": GWAS_EFO_EBI,
    "GWAS_NLP": GWAS_NLP,
    "GWAS_NLP_EFO": GWAS_NLP_EFO,
    "GWAS_TO_LITERATURE": GWAS_TO_LITERATURE,
    "GWAS_TO_LITERATURE_TRIPLE": GWAS_TO_LITERATURE_TRIPLE,
    "GWAS_TO_VARIANT": GWAS_TO_VARIANT,
    "MEDRXIV_OBJ": MEDRXIV_OBJ,
    "MEDRXIV_PREDICATE": MEDRXIV_PREDICATE,
    "MEDRXIV_SUB": MEDRXIV_SUB,
    "MEDRXIV_TO_LIT": MEDRXIV_TO_LIT,
    "METAMAP_LITE": METAMAP_LITE,
    "MONDO_MAP_EFO": MONDO_MAP_EFO,
    "MONDO_MAP_UMLS": MONDO_MAP_UMLS,
    "MR_EVE_MR": MR_EVE_MR,
    "OBS_COR": OBS_COR,
    "OPENTARGETS_DRUG_TO_DISEASE": OPENTARGETS_DRUG_TO_DISEASE,
    "OPENTARGETS_DRUG_TO_TARGET": OPENTARGETS_DRUG_TO_TARGET,
    "PATHWAY_CHILD_OF": PATHWAY_CHILD_OF,
    "PROTEIN_IN_PATHWAY": PROTEIN_IN_PATHWAY,
    "PRS": PRS,
    "TERM_TO_GENE": TERM_TO_GENE,
    "SEMMEDDB_OBJ": SEMMEDDB_OBJ,
    "SEMMEDDB_PREDICATE": SEMMEDDB_PREDICATE,
    "SEMMEDDB_SUB": SEMMEDDB_SUB,
    "SEMMEDDB_TO_LIT": SEMMEDDB_TO_LIT,
    "STRING_INTERACT_WITH": STRING_INTERACT_WITH,
    "OPENGWAS_TOPHITS": OPENGWAS_TOPHITS,
    "VARIANT_TO_GENE": VARIANT_TO_GENE,
    "XQTL_MULTI_SNP_MR": XQTL_MULTI_SNP_MR,
    "XQTL_SINGLE_SNP_MR_GENE_GWAS": XQTL_SINGLE_SNP_MR_GENE_GWAS,
    "XQTL_SINGLE_SNP_MR_SNP_GENE": XQTL_SINGLE_SNP_MR_SNP_GENE,
    "GENE_TO_DISEASE": GENE_TO_DISEASE,
}

meta_path_schema = {
    key: (value._Path.source, value._Path.target)  # type: ignore
    for key, value in meta_rel_schema.items()
}

from typing import List, Optional

from app.utils.schema import Neo4jEntity


class BN_GEN_COR(Neo4jEntity):
    """Study results from "UKBB Genetic Correlation" project
    by Neale Lab.
    """

    rg: float
    se: float
    z: float
    p: float
    h2_obs: float
    h2_obs_se: float
    h2_int: float
    h2_int_se: float
    gcov_int: float
    gcov_int_se: float

    class _Path:
        source = "Gwas"
        target = "Gwas"


class CPIC(Neo4jEntity):
    pharmgkb_level_of_evidence: str
    cpic_level: str
    guideline: str
    pgx_on_fda_label: str

    class _Path:
        source = "Drug"
        target = "Gene"


class EFO_CHILD_OF(Neo4jEntity):
    class _Path:
        source = "Efo"
        target = "Efo"


class EVENT_IN_PATHWAY(Neo4jEntity):
    class _Path:
        source = "Pathway"
        target = "Event"


class EXPRESSED_IN(Neo4jEntity):
    tpm: float

    class _Path:
        source = "Gene"
        target = "Tissue"


class GENE_TO_LITERATURE(Neo4jEntity):
    class _Path:
        source = "Gene"
        target = "Literature"


class GENE_TO_PROTEIN(Neo4jEntity):
    class _Path:
        source = "Gene"
        target = "Protein"


class GWAS_NLP(Neo4jEntity):
    """Pairwise semantic similarity of GWAS traits.

    Precomputed results from Vectology (BioSentVec model).
    """

    score: float

    class _Path:
        source = "Gwas"
        target = "Gwas"


class GWAS_NLP_EFO(Neo4jEntity):
    """Semantic similarity of a GWAS trait to an EFO term.

    Precomputed results from Vectology (BioSentVec model).
    """

    score: float

    class _Path:
        source = "Gwas"
        target = "Efo"


class GWAS_SEM(Neo4jEntity):
    localCount: int
    localTotal: int
    globalCount: int
    globalTotal: int
    odds: float
    pval: float

    class _Path:
        source = "Gwas"
        target = "SemmedTriple"


class GWAS_TO_LIT(Neo4jEntity):
    class _Path:
        source = "Gwas"
        target = "Literature"


class GWAS_TO_VARIANT(Neo4jEntity):
    beta: float
    se: Optional[float]
    pval: float
    eaf: Optional[float]
    samplesize: float
    ncase: Optional[int]
    ncontrol: Optional[int]

    class _Path:
        source = "Gwas"
        target = "Variant"


class INTACT_INTERACTS_WITH_GENE_GENE(Neo4jEntity):
    intact_confidence_score: float
    intact_detection_method: List[str]
    intact_type: List[str]
    intact_source: List[str]
    intact_identifier: List[str]

    class _Path:
        source = "Gene"
        target = "Gene"


class INTACT_INTERACTS_WITH_PROTEIN_PROTEIN(Neo4jEntity):
    intact_confidence_score: float
    intact_detection_method: List[str]
    intact_type: List[str]
    intact_source: List[str]
    intact_identifier: List[str]

    class _Path:
        source = "Protein"
        target = "Protein"


class INTACT_INTERACTS_WITH_GENE_PROTEIN(Neo4jEntity):
    intact_confidence_score: float
    intact_detection_method: List[str]
    intact_type: List[str]
    intact_source: List[str]
    intact_identifier: List[str]

    class _Path:
        source = "Gene"
        target = "Protein"


class INTACT_NOT_INTERACTS_WITH(Neo4jEntity):
    intact_confidence_score: float
    intact_detection_method: List[str]
    intact_type: List[str]
    intact_source: List[str]
    intact_identifier: List[str]

    class _Path:
        source = "Protein"
        target = "Protein"


class METAMAP_LITE(Neo4jEntity):
    """Mapping between Gwas and SemmedTerm via MetaMap Lite.
    """

    mmi_score: float

    class _Path:
        source = "Gwas"
        target = "SemmedTerm"


class MONDO_MAP_EFO(Neo4jEntity):
    class _Path:
        source = "Disease"
        target = "Efo"


class MONDO_MAP_UMLS(Neo4jEntity):
    class _Path:
        source = "Disease"
        target = "SemmedTerm"


class MR(Neo4jEntity):
    """Pairwise Mendelian randomization evidence.

    Results from MR-EvE.
    """

    # TODO: review
    method: str
    nsnp: float
    b: float
    se: Optional[float]
    ci_low: Optional[float]
    ci_upp: Optional[float]
    pval: Optional[float]
    selection: str
    moescore: str
    log10pval: Optional[float]

    class Config:
        extra = "forbid"

    class _Path:
        source = "Gwas"
        target = "Gwas"


class OBS_COR(Neo4jEntity):
    """Pairwise Spearman rank correlation for UK Biobank GWAS (ukb-b).

    Results in-house by Benjamin Elsworth.
    """

    cor: float

    class _Path:
        source = "Gwas"
        target = "Gwas"


class OPENTARGETS_DRUG_TO_DISEASE(Neo4jEntity):
    class _Path:
        source = "Drug"
        target = "Disease"


class OPENTARGETS_DRUG_TO_TARGET(Neo4jEntity):
    phase: str
    action_type: str

    class _Path:
        source = "Drug"
        target = "Gene"


class PATHWAY_TO_DISEASE(Neo4jEntity):
    class _Path:
        source = "Pathway"
        target = "Disease"


class PATHWAY_TO_LITERATURE(Neo4jEntity):
    class _Path:
        source = "Pathway"
        target = "Literature"


class PRECEDING_EVENT(Neo4jEntity):
    class _Path:
        source = "Event"
        target = "Event"


class PROTEIN_IN_EVENT(Neo4jEntity):
    class _Path:
        source = "Protein"
        target = "Event"


class PROTEIN_TO_DISEASE(Neo4jEntity):
    class _Path:
        source = "Protein"
        target = "Disease"


class PROTEIN_TO_LITERATURE(Neo4jEntity):
    class _Path:
        source = "Protein"
        target = "Literature"


class PROTEIN_IN_PATHWAY(Neo4jEntity):
    class _Path:
        source = "Protein"
        target = "Pathway"


class PRS(Neo4jEntity):
    """Pairwise polygenic risk scores between GWAS.

    Results from PRS Atlas.
    """

    nsnps: int
    model: str
    beta: float
    se: float
    p: float
    r2: float
    n: int

    class _Path:
        source = "Gwas"
        target = "Gwas"


class SEM_GENE(Neo4jEntity):
    class _Path:
        source = "SemmedTerm"
        target = "Gene"


class SEM_OBJ(Neo4jEntity):
    class _Path:
        source = "SemmedTriple"
        target = "SemmedTerm"


class SEM_PREDICATE(Neo4jEntity):
    predicate: str
    count: int

    class _Path:
        source = "SemmedTerm"
        target = "SemmedTerm"


class SEM_SUB(Neo4jEntity):
    class _Path:
        source = "SemmedTriple"
        target = "SemmedTerm"


class SEM_TO_LIT(Neo4jEntity):
    class _Path:
        source = "SemmedTriple"
        target = "Literature"


class STRING_INTERACT_WITH(Neo4jEntity):
    score: float

    class _Path:
        source = "Protein"
        target = "Protein"


class TOPHITS(Neo4jEntity):
    beta: float
    pval: float

    class _Path:
        source = "Gwas"
        target = "Variant"


class VARIANT_TO_GENE(Neo4jEntity):
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


class XQTL_MULTI_SNP_MR(Neo4jEntity):
    """Association of exposure gene and outcome phenotype in the multi SNP MR results of xQTL.
    """

    beta: float
    se: float
    p: float
    qtl_type: str
    mr_method: str

    class _Path:
        source = "Gene"
        target = "Gwas"


class XQTL_SINGLE_SNP_MR_GENE_GWAS(Neo4jEntity):
    """Association of exposure gene and outcome phenotype in the single SNP MR results of xQTL.
    """

    beta: float
    se: float
    p: float
    rsid: str
    qtl_type: str

    class _Path:
        source = "Gene"
        target = "Gwas"


class XQTL_SINGLE_SNP_MR_SNP_GENE(Neo4jEntity):
    """Association of SNP and exposure gene in the single SNP MR results of xQTL.
    """

    class _Path:
        source = "Variant"
        target = "Gene"


meta_rel_schema = {
    "BN_GEN_COR": BN_GEN_COR,
    "CPIC": CPIC,
    "EFO_CHILD_OF": EFO_CHILD_OF,
    "EVENT_IN_PATHWAY": EVENT_IN_PATHWAY,
    "EXPRESSED_IN": EXPRESSED_IN,
    "GENE_TO_LITERATURE": GENE_TO_LITERATURE,
    "GENE_TO_PROTEIN": GENE_TO_PROTEIN,
    "GWAS_NLP": GWAS_NLP,
    "GWAS_NLP_EFO": GWAS_NLP_EFO,
    "GWAS_SEM": GWAS_SEM,
    "GWAS_TO_LIT": GWAS_TO_LIT,
    "GWAS_TO_VARIANT": GWAS_TO_VARIANT,
    "INTACT_INTERACTS_WITH_GENE_GENE": INTACT_INTERACTS_WITH_GENE_GENE,
    "INTACT_INTERACTS_WITH_GENE_PROTEIN": INTACT_INTERACTS_WITH_GENE_PROTEIN,
    "INTACT_INTERACTS_WITH_PROTEIN_PROTEIN": INTACT_INTERACTS_WITH_PROTEIN_PROTEIN,
    "INTACT_NOT_INTERACTS_WITH": INTACT_NOT_INTERACTS_WITH,
    "METAMAP_LITE": METAMAP_LITE,
    "MONDO_MAP_EFO": MONDO_MAP_EFO,
    "MONDO_MAP_UMLS": MONDO_MAP_UMLS,
    "MR": MR,
    "OBS_COR": OBS_COR,
    "OPENTARGETS_DRUG_TO_DISEASE": OPENTARGETS_DRUG_TO_DISEASE,
    "OPENTARGETS_DRUG_TO_TARGET": OPENTARGETS_DRUG_TO_TARGET,
    "PATHWAY_TO_DISEASE": PATHWAY_TO_DISEASE,
    "PATHWAY_TO_LITERATURE": PATHWAY_TO_LITERATURE,
    "PRECEDING_EVENT": PRECEDING_EVENT,
    "PROTEIN_IN_EVENT": PROTEIN_IN_EVENT,
    "PROTEIN_TO_DISEASE": PROTEIN_TO_DISEASE,
    "PROTEIN_TO_LITERATURE": PROTEIN_TO_LITERATURE,
    "PROTEIN_IN_PATHWAY": PROTEIN_IN_PATHWAY,
    "PRS": PRS,
    "SEM_GENE": SEM_GENE,
    "SEM_OBJ": SEM_OBJ,
    "SEM_PREDICATE": SEM_PREDICATE,
    "SEM_SUB": SEM_SUB,
    "SEM_TO_LIT": SEM_TO_LIT,
    "STRING_INTERACT_WITH": STRING_INTERACT_WITH,
    "TOPHITS": TOPHITS,
    "VARIANT_TO_GENE": VARIANT_TO_GENE,
    "XQTL_MULTI_SNP_MR": XQTL_MULTI_SNP_MR,
    "XQTL_SINGLE_SNP_MR_GENE_GWAS": XQTL_SINGLE_SNP_MR_GENE_GWAS,
    "XQTL_SINGLE_SNP_MR_SNP_GENE": XQTL_SINGLE_SNP_MR_SNP_GENE,
}

# TODO: how to solve Type[BaseModel] has no attribute _Path?
#       do we need a dedicated child class?
meta_path_schema = {
    key: (value._Path.source, value._Path.target)  # type: ignore
    for key, value in meta_rel_schema.items()
}

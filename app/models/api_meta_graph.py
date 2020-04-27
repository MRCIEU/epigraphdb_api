from enum import Enum


class EpigraphdbMetaNodesFull(str, Enum):
    """The version with special nodes included"""

    Gwas = "Gwas"
    Disease = "Disease"
    Drug = "Drug"
    Efo = "Efo"
    Event = "Event"
    Gene = "Gene"
    Tissue = "Tissue"
    Literature = "Literature"
    Pathway = "Pathway"
    Protein = "Protein"
    SemmedTerm = "SemmedTerm"
    SemmedTriple = "SemmedTriple"
    Variant = "Variant"
    Meta = "Meta"


class EpigraphdbMetaNodes(str, Enum):
    """The version without special nodes included"""

    Gwas = "Gwas"
    Disease = "Disease"
    Drug = "Drug"
    Efo = "Efo"
    Event = "Event"
    Gene = "Gene"
    Tissue = "Tissue"
    Literature = "Literature"
    Pathway = "Pathway"
    Protein = "Protein"
    SemmedTerm = "SemmedTerm"
    Variant = "Variant"


class EpigraphdbMetaRels(str, Enum):
    BN_GEN_COR = "BN_GEN_COR"
    CPIC = "CPIC"
    EFO_CHILD_OF = "EFO_CHILD_OF"
    EVENT_IN_PATHWAY = "EVENT_IN_PATHWAY"
    EXPRESSED_IN = "EXPRESSED_IN"
    GENE_TO_LITERATURE = "GENE_TO_LITERATURE"
    GENE_TO_PROTEIN = "GENE_TO_PROTEIN"
    GWAS_NLP = "GWAS_NLP"
    GWAS_NLP_EFO = "GWAS_NLP_EFO"
    GWAS_SEM = "GWAS_SEM"
    GWAS_TO_LIT = "GWAS_TO_LIT"
    GWAS_TO_VARIANT = "GWAS_TO_VARIANT"
    INTACT_INTERACTS_WITH_GENE_GENE = "INTACT_INTERACTS_WITH_GENE_GENE"
    INTACT_INTERACTS_WITH_GENE_PROTEIN = "INTACT_INTERACTS_WITH_GENE_PROTEIN"
    INTACT_INTERACTS_WITH_PROTEIN_PROTEIN = (
        "INTACT_INTERACTS_WITH_PROTEIN_PROTEIN"
    )
    INTACT_NOT_INTERACTS_WITH = "INTACT_NOT_INTERACTS_WITH"
    METAMAP_LITE = "METAMAP_LITE"
    MONDO_MAP_EFO = "MONDO_MAP_EFO"
    MONDO_MAP_UMLS = "MONDO_MAP_UMLS"
    MR = "MR"
    OBS_COR = "OBS_COR"
    OPENTARGETS_DRUG_TO_DISEASE = "OPENTARGETS_DRUG_TO_DISEASE"
    OPENTARGETS_DRUG_TO_TARGET = "OPENTARGETS_DRUG_TO_TARGET"
    PATHWAY_TO_DISEASE = "PATHWAY_TO_DISEASE"
    PATHWAY_TO_LITERATURE = "PATHWAY_TO_LITERATURE"
    PRECEDING_EVENT = "PRECEDING_EVENT"
    PROTEIN_IN_EVENT = "PROTEIN_IN_EVENT"
    PROTEIN_IN_PATHWAY = "PROTEIN_IN_PATHWAY"
    PROTEIN_TO_DISEASE = "PROTEIN_TO_DISEASE"
    PROTEIN_TO_LITERATURE = "PROTEIN_TO_LITERATURE"
    PRS = "PRS"
    SEM_GENE = "SEM_GENE"
    SEM_OBJ = "SEM_OBJ"
    SEM_PREDICATE = "SEM_PREDICATE"
    SEM_SUB = "SEM_SUB"
    SEM_TO_LIT = "SEM_TO_LIT"
    STRING_INTERACT_WITH = "STRING_INTERACT_WITH"
    TOPHITS = "TOPHITS"
    VARIANT_TO_GENE = "VARIANT_TO_GENE"
    XQTL_MULTI_SNP_MR = "XQTL_MULTI_SNP_MR"
    XQTL_SINGLE_SNP_MR_GENE_GWAS = "XQTL_SINGLE_SNP_MR_GENE_GWAS"
    XQTL_SINGLE_SNP_MR_SNP_GENE = "XQTL_SINGLE_SNP_MR_SNP_GENE"
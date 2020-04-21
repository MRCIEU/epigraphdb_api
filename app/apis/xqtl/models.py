from enum import Enum
from typing import List

from pydantic import BaseModel

from app.models import ApiMetadata
from app.models.output_nodes import TraitItem


class XqtlListMetaNodeInput(str, Enum):
    # NOTE: We are not able to query
    #       for full list of snps in a simple way
    #       to do that loop over snps used in all
    #       gwas
    gene = "Gene"
    gwas = "Gwas"
    gene_gwas = "GeneGwas"


class MrMethodInput(str, Enum):
    ivw = "IVW"
    egger = "Egger"


class QtlTypeInput(str, Enum):
    eqtl = "eQTL"
    pqtl = "pQTL"


class GeneByVariantRequest(BaseModel):
    variant_list: List[str]
    qtl_type: QtlTypeInput = QtlTypeInput.eqtl


class XqtlGeneItem(BaseModel):
    ensembl_id: str
    name: str


class XqtlMultiSnpMrItem(BaseModel):
    beta: float
    se: float
    p: float


class XqtlSingleSnpMrItem(BaseModel):
    beta: float
    se: float
    p: float
    rsid: str


class XqtlMultiSnpMrResultItem(BaseModel):
    gene: XqtlGeneItem
    gwas: TraitItem
    r: XqtlMultiSnpMrItem


class XqtlSingleSnpMrResultItem(BaseModel):
    gene: XqtlGeneItem
    gwas: TraitItem
    r: XqtlSingleSnpMrItem


class XqtlMultiSnpMrResponse(BaseModel):
    metadata: ApiMetadata
    results: List[XqtlMultiSnpMrResultItem]


class XqtlSingleSnpMrSnpResponse(BaseModel):
    metadata: ApiMetadata
    results: List[XqtlSingleSnpMrResultItem]

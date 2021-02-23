from typing import Optional

from pydantic import BaseModel


class MRItem(BaseModel):
    b: float
    se: float
    pval: float
    method: str
    selection: str
    moescore: float


class ObsCorItem(BaseModel):
    cor: float


class GeneticCorItem(BaseModel):
    Z: float
    p: float
    rg: float
    rg_SE: Optional[float] = None
    rg_intercept: Optional[float] = None
    rg_intercept_SE: Optional[float] = None
    h2: Optional[float] = None
    h2_SE: Optional[float] = None
    h2_intercept: Optional[float] = None
    h2_intercept_SE: Optional[float] = None


class GwasToVariantItem(BaseModel):
    beta: float
    se: float
    pval: float
    # TODO: update these
    # eaf: Optional[float]
    samplesize: float


class PrsItem(BaseModel):
    Beta: float
    SE: float
    P: float
    r2: float
    Model: str
    nSNPs: int
    N: int


class OpentargetsDrugToTargetItem(BaseModel):
    phase: str
    action_type: str


class CpicItem(BaseModel):
    pharmgkb_level_of_evidence: str
    pgx_on_fda_label: str
    cpic_level: str
    guideline: str

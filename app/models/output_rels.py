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


class BNGeneticCorItem(BaseModel):
    rg: float
    z: float
    se: float
    p: float
    h2_int: float
    h2_int_se: float
    h2_obs: float
    h2_obs_se: float
    gcov_int: float
    gcov_int_se: float


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

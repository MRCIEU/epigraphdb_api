from fastapi import APIRouter, Query

from app.settings import epigraphdb
from app.utils.logging import log_args

from .models import RiskFactorsResponse
from .queries import DrugsQueries

router = APIRouter()


@router.get("/drugs/risk-factors", response_model=RiskFactorsResponse)
def get_drugs_risk_factors(
    trait: str = None, pval_threshold: float = Query(1e-8, ge=0.0, le=1.0)
):
    """
    Drugs for common risk factors of diseases
    """
    log_args(api="/drugs/risk-factors", kwargs=locals())
    query = DrugsQueries.risk_factors.format(
        trait=trait, pval_threshold=pval_threshold
    )
    response = epigraphdb.run_query(query)
    return response

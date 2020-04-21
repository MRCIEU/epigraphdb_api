from typing import Optional

from fastapi import APIRouter, Query

from app.settings import epigraphdb
from app.utils.logging import log_args
from app.utils.validators import validate_at_least_one_not_none

from .models import MRResponse
from .queries import MRQueries

router = APIRouter()


@router.get("/mr", response_model=MRResponse)
def get_mr(
    exposure_trait: Optional[str] = None,
    outcome_trait: Optional[str] = None,
    pval_threshold: float = Query(1e-5, ge=0.0, le=1.0),
):
    """
    Return information related to Mendelian randomisation

    Specify at least one of `exposure_trait` and `outcome_trait`
    or both.
    """
    log_args(api="/mr", kwargs=locals())
    validate_at_least_one_not_none(
        dict(exposure_trait=exposure_trait, outcome_trait=outcome_trait)
    )
    if exposure_trait is not None and outcome_trait is not None:
        query = MRQueries.pair.format(
            exposure_trait=exposure_trait,
            outcome_trait=outcome_trait,
            pval_threshold=pval_threshold,
        )
        res = epigraphdb.run_query(query)
    elif exposure_trait is not None:
        query = MRQueries.exp.format(
            exposure_trait=exposure_trait, pval_threshold=pval_threshold
        )
        res = epigraphdb.run_query(query)
    elif outcome_trait is not None:
        query = MRQueries.out.format(
            outcome_trait=outcome_trait, pval_threshold=pval_threshold
        )
        res = epigraphdb.run_query(query)
    return res

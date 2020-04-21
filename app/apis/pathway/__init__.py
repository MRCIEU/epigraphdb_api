from fastapi import APIRouter, Query

from app.settings import epigraphdb
from app.utils.logging import log_args

from .models import PathwayResponse
from .queries import PathwayQueries

router = APIRouter()


@router.get("/pathway", response_model=PathwayResponse)
def get_pathway(
    trait: str, pval_threshold: float = Query(1e-5, ge=0.0, le=1.0)
):
    """
    Pathway-based stratification of instruments
    """
    log_args(api="/pathway", kwargs=locals())
    query = PathwayQueries.pathway.format(
        trait=trait, pval_threshold=pval_threshold
    )
    response = epigraphdb.run_query(query)
    return response

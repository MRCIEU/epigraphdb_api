"""Currently deprecated
"""
from fastapi import APIRouter, Query

from app.settings import epigraphdb
from app.utils.logging import log_args

from .models import GeneticCorResponse
from .queries import GeneticCorQueries

router = APIRouter()


@router.get("/genetic-cor", response_model=GeneticCorResponse)
def get_genetic_cor(
    trait: str, cor_coef_threshold: float = Query(0.8, ge=-1.0, le=1.0)
):
    """
    Returns genetic correlates for a trait.

    Args:

    - `trait`: A trait name, e.g. Whole body fat mass
    - `cor_coef_threshold`: correlation coefficient threshold
    """
    log_args(api="/genetic-cor", kwargs=locals())
    query = GeneticCorQueries.genetic_cor.format(
        trait=trait, cor_coef_threshold=cor_coef_threshold
    )
    response = epigraphdb.run_query(query)
    return response

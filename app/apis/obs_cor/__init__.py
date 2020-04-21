from fastapi import APIRouter, Query

from app.settings import epigraphdb
from app.utils.logging import log_args

from .models import ObsCorResponse
from .queries import ObsCorQueries

router = APIRouter()


@router.get("/obs-cor", response_model=ObsCorResponse)
def get_obs_cor(
    trait: str, cor_coef_threshold: float = Query(0.8, ge=-1.0, le=1.0)
):
    """
    Returns observational correlates for a trait.

    Args:
    - `trait`: A trait name, e.g. "body mass index"
    - `cor_coef_threshold`: Coefficient correlation threshold
    """
    log_args(api="/obs-cor", kwargs=locals())
    query = ObsCorQueries.gwas_obs_cor.format(
        trait=trait, cor_coef_threshold=cor_coef_threshold
    )
    response = epigraphdb.run_query(query)
    return response

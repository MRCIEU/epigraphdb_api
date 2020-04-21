from fastapi import APIRouter, Query

from app.settings import epigraphdb
from app.utils.logging import log_args

from .queries import PrsQueries

router = APIRouter()


@router.get("/prs")
def get_prs(trait: str, pval_threshold: float = Query(1e-5, ge=0.0, le=1.0)):
    """Polygenic risk scores between GWAS traits
    """
    log_args(api="/prs", kwargs=locals())
    query = PrsQueries.prs.format(trait=trait, pval_threshold=pval_threshold)
    response = epigraphdb.run_query(query)
    return response

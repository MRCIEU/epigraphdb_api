from enum import Enum
from typing import Optional

from fastapi import APIRouter, Query

from app.settings import epigraphdb
from app.utils.logging import log_args
from app.utils.validators import validate_at_least_one_not_none

from .models import ConfounderResponse
from .queries import ConfounderQueries

router = APIRouter()


class ConfounderType(str, Enum):
    confounder = "confounder"
    intermediate = "intermediate"
    reverse_intermediate = "reverse_intermediate"
    collider = "collider"


@router.get("/confounder", response_model=ConfounderResponse)
def get_confounder(
    exposure_trait: Optional[str] = None,
    outcome_trait: Optional[str] = None,
    type: ConfounderType = ConfounderType.confounder,
    pval_threshold: float = Query(1e-5, ge=0.0, le=1.0),
):
    """
    Get confounder / intermediate / collider evidence between traits:

    `type` accepts 1 of the 4 options:

    - confounder: confounder->exposure->outcome<-confounder
    - intermediate: intermediate<-exposure->outcome<-confounder
    - reverse_intermediate: intermediate->exposure->outcome->confounder
    - collider: collider<-exposure->outcome->collider
    """
    log_args(api="/confounder", kwargs=locals())
    validate_at_least_one_not_none(
        dict(exposure_trait=exposure_trait, outcome_trait=outcome_trait)
    )
    if type == "confounder":
        query = ConfounderQueries.confounder.format(
            exposure_trait=exposure_trait,
            outcome_trait=outcome_trait,
            pval_threshold=pval_threshold,
        )
    elif type == "intermediate":
        query = ConfounderQueries.intermediate.format(
            exposure_trait=exposure_trait,
            outcome_trait=outcome_trait,
            pval_threshold=pval_threshold,
        )
    elif type == "reverse_intermediate":
        query = ConfounderQueries.reverse_intermediate.format(
            exposure_trait=exposure_trait,
            outcome_trait=outcome_trait,
            pval_threshold=pval_threshold,
        )
    elif type == "collider":
        query = ConfounderQueries.collider.format(
            exposure_trait=exposure_trait,
            outcome_trait=outcome_trait,
            pval_threshold=pval_threshold,
        )
    response = epigraphdb.run_query(query)
    return response

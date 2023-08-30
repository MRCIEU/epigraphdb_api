import sqlite3
from typing import Optional

import pandas as pd
from fastapi import APIRouter

from app.models import ApiGenericResponse
from app.resources.dependent_files import dependent_files
from app.utils.process_query import format_response

from . import models

router = APIRouter()

MASTER_ROUTE = "sc_eqtl_mr"


@router.get(
    f"/{MASTER_ROUTE}/list/{{entity}}",
    response_model=ApiGenericResponse,
)
def list_ents(entity: models.Entity):
    """List entities"""
    query = "SELECT * FROM {entity}".format(entity=entity.value)
    with sqlite3.connect(dependent_files["sc-eqtl-mr"]) as conn:
        data = (
            pd.read_sql(query, conn)
            .drop(columns=["idx"])
            .to_dict(orient="records")
        )
    res = format_response(data=data)
    return res


@router.get(
    f"/{MASTER_ROUTE}/query/{{entity}}",
    response_model=ApiGenericResponse,
)
def main_query(
    entity: models.Entity,
    q: Optional[str] = None,
    pval_threshold: float = 1e-3,
):
    """Main MR evidence"""
    _query_common = """
        SELECT * FROM MAIN_DATA
        WHERE pval < {pval_threshold}
    """
    if entity.value == "outcome":
        query = _query_common + "AND outcome_id = '{q}';"
    elif entity.value == "gene":
        query = _query_common + "AND gene_id = '{q}';"
    query = query.format(q=q, pval_threshold=pval_threshold).replace("\n", " ")
    with sqlite3.connect(dependent_files["sc-eqtl-mr"]) as conn:
        data = (
            pd.read_sql(query, conn)
            .drop(columns=["idx"])
            .to_dict(orient="records")
        )
    res = format_response(data=data)
    return res

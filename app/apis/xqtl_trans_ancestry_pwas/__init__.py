import sqlite3
from typing import Optional

import numpy as np
import pandas as pd
from fastapi import APIRouter

from app.models import ApiGenericResponse
from app.resources.dependent_files import dependent_files
from app.utils.process_query import format_response

from . import models

router = APIRouter()


@router.get(
    "/xqtl_trans_ancestry_pwas/list/{entity}", response_model=ApiGenericResponse
)
def list_ents(entity: models.Entity):
    """List entities"""
    query = "SELECT * FROM {entity}".format(entity=entity.value)
    with sqlite3.connect(dependent_files["xqtl_pwas_mr"]) as conn:
        data = pd.read_sql(query, conn).drop(columns=["idx"]).to_dict(orient="records")
    res = format_response(data=data)
    return res


@router.get(
    "/xqtl_trans_ancestry_pwas/xqtl_pwas_mr/{entity}",
    response_model=ApiGenericResponse,
)
def xqtl_pwas_mr(
    entity: models.Entity,
    q: Optional[str] = None,
    pval_threshold: float = 1e-3,
):
    """Main MR evidence"""
    _query_common = """
        SELECT *
        FROM XQTL_PWAS_MR
        WHERE
          pval < {pval_threshold}
    """
    if entity.value == "gwas":
        query = _query_common + "AND gwas_id = '{q}';"
    elif entity.value == "gene":
        query = _query_common + "AND gene_id = '{q}';"
    query = query.format(q=q, pval_threshold=pval_threshold).replace("\n", " ")
    with sqlite3.connect(dependent_files["xqtl_pwas_mr"]) as conn:
        res_df = pd.read_sql(query, conn).drop(columns=["idx"]).replace({np.nan: None})
    data = res_df.to_dict(orient="records")
    res = format_response(data=data)
    return res

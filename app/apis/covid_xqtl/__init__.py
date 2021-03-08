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


@router.get("/covid-19/ctda/list/{entity}", response_model=ApiGenericResponse)
def get_list_gwas(entity: models.CovidXqtlList):
    """List entities"""
    query = "SELECT * FROM {entity}".format(entity=entity.value)
    with sqlite3.connect(dependent_files["covid-xqtl"]) as conn:
        data = pd.read_sql(query, conn).to_dict(orient="records")
    res = format_response(data=data)
    return res


@router.get(
    "/covid-19/ctda/single-snp-mr/{entity}", response_model=ApiGenericResponse
)
def get_single_snp_mr(
    entity: models.CovidXqtlSingleSnpMrEntity,
    q: Optional[str] = None,
    pval_threshold: float = 1e-3,
):
    """Single SNP MR"""
    _query_common = """
        SELECT *
        FROM single_snp_mr
        WHERE
          p < {pval_threshold}
    """
    if entity.value == "tissue":
        query = _query_common + "AND tissue = '{q}';"
    elif entity.value == "gwas":
        query = _query_common + "AND outcome_id = '{q}';"
    elif entity.value == "gene":
        query = _query_common + "AND exposure_id = '{q}';"
    elif entity.value == "snp":
        query = _query_common + "AND SNP = '{q}';"
    query = query.format(q=q, pval_threshold=pval_threshold).replace("\n", " ")
    with sqlite3.connect(dependent_files["covid-xqtl"]) as conn:
        res_df = pd.read_sql(query, conn).replace({np.nan: None})
    data = res_df.to_dict(orient="records")
    res = format_response(data=data)
    return res


@router.get(
    "/covid-19/ctda/multi-snp-mr/{entity}", response_model=ApiGenericResponse
)
def get_multi_snp_mr(
    entity: models.CovidXqtlMultiSnpMrEntity,
    q: Optional[str] = None,
    pval_threshold: float = 1e-3,
):
    """Multi SNP MR"""
    _query_common = """
        SELECT *
        FROM multi_snp_mr
        WHERE
          p < {pval_threshold}
    """
    if entity.value == "tissue":
        query = _query_common + "AND tissue = '{q}';"
    elif entity.value == "gwas":
        query = _query_common + "AND outcome_id = '{q}';"
    elif entity.value == "gene":
        query = _query_common + "AND exposure_id = '{q}';"
    query = query.format(q=q, pval_threshold=pval_threshold).replace("\n", " ")
    with sqlite3.connect(dependent_files["covid-xqtl"]) as conn:
        res_df = pd.read_sql(query, conn).replace({np.nan: None})
    data = res_df.to_dict(orient="records")
    res = format_response(data=data)
    return res

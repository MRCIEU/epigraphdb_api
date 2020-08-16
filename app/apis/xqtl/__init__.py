from typing import List, Optional

import pandas as pd
from fastapi import APIRouter, Query

from app.resources.dependent_files import dependent_files
from app.settings import epigraphdb
from app.utils.logging import log_args
from app.utils.validators import validate_at_least_one_not_none

from . import queries as xqtl_queries
from .models import (
    GeneByVariantRequest,
    MrMethodInput,
    QtlTypeInput,
    XqtlListMetaNodeInput,
    XqtlMultiSnpMrResponse,
    XqtlSingleSnpMrSnpResponse,
)

router = APIRouter()


with open(dependent_files["gene_id_exclude"], "r") as f:
    pqtl_gene_exclude = [_.strip() for _ in f]


@router.get("/xqtl/multi-snp-mr", response_model=XqtlMultiSnpMrResponse)
def get_xqtl_multi_snp_mr(
    exposure_gene: Optional[str] = None,
    outcome_trait: Optional[str] = None,
    mr_method: MrMethodInput = MrMethodInput.ivw,
    qtl_type: QtlTypeInput = QtlTypeInput.eqtl,
    pval_threshold: float = Query(1e-5, ge=0.0, le=1.0),
):
    """xQTL multi SNP MR results

    Search by exposure_gene, outcome_trait, or both.

    - qtl_type: eQTL, pQTL
    """
    log_args(api="/xqtl/multi-snp-mr", kwargs=locals())
    validate_at_least_one_not_none(
        dict(exposure_gene=exposure_gene, outcome_trait=outcome_trait)
    )
    if exposure_gene is not None and outcome_trait is not None:
        query = xqtl_queries.XqtlMultiSnpMr.exposure_outcome.format(
            exposure=exposure_gene,
            outcome=outcome_trait,
            mr_method=mr_method.value,
            qtl_type=qtl_type.value,
            pval_threshold=pval_threshold,
        )
    elif exposure_gene is not None:
        query = xqtl_queries.XqtlMultiSnpMr.exposure.format(
            exposure=exposure_gene,
            mr_method=mr_method.value,
            qtl_type=qtl_type.value,
            pval_threshold=pval_threshold,
        )
    elif outcome_trait is not None:
        query = xqtl_queries.XqtlMultiSnpMr.outcome.format(
            outcome=outcome_trait,
            mr_method=mr_method.value,
            qtl_type=qtl_type.value,
            pval_threshold=pval_threshold,
        )
    response = epigraphdb.run_query(query)
    if qtl_type.value == "pQTL" and len(response["results"]) > 0:
        response = mask_pqtl_snp(response=response, id_list=pqtl_gene_exclude)
    return response


@router.get("/xqtl/single-snp-mr", response_model=XqtlSingleSnpMrSnpResponse)
def get_xqtl_single_snp_mr(
    exposure_gene: str = None,
    outcome_trait: str = None,
    variant: str = None,
    qtl_type: QtlTypeInput = QtlTypeInput.eqtl,
    pval_threshold: float = 1e-5,
):
    """xQTL single SNP MR results

    Search by exposure_gene, outcome_trait, variant, or all of them.

    - qtl_type: eQTL, pQTL
    """
    log_args(api="/xqtl/single-snp-mr", kwargs=locals())
    validate_at_least_one_not_none(
        dict(
            exposure_gene=exposure_gene,
            outcome_trait=outcome_trait,
            variant=variant,
        )
    )
    if (
        exposure_gene is not None
        and outcome_trait is not None
        and variant is not None
    ):
        query = xqtl_queries.XqtlSingleSnpMr.exposure_outcome_snp.format(
            exposure=exposure_gene,
            outcome=outcome_trait,
            variant=variant,
            qtl_type=qtl_type.value,
            pval_threshold=pval_threshold,
        )
    elif exposure_gene is not None and outcome_trait is not None:
        query = xqtl_queries.XqtlSingleSnpMr.exposure_outcome.format(
            exposure=exposure_gene,
            outcome=outcome_trait,
            qtl_type=qtl_type.value,
            pval_threshold=pval_threshold,
        )
    elif exposure_gene is not None and variant is not None:
        query = xqtl_queries.XqtlSingleSnpMr.exposure_snp.format(
            exposure=exposure_gene,
            variant=variant,
            qtl_type=qtl_type.value,
            pval_threshold=pval_threshold,
        )
    elif outcome_trait is not None and variant is not None:
        query = xqtl_queries.XqtlSingleSnpMr.outcome_snp.format(
            outcome=outcome_trait,
            variant=variant,
            qtl_type=qtl_type.value,
            pval_threshold=pval_threshold,
        )
    elif exposure_gene is not None:
        query = xqtl_queries.XqtlSingleSnpMr.exposure.format(
            exposure=exposure_gene,
            qtl_type=qtl_type.value,
            pval_threshold=pval_threshold,
        )
    elif outcome_trait is not None:
        query = xqtl_queries.XqtlSingleSnpMr.outcome.format(
            outcome=outcome_trait,
            qtl_type=qtl_type.value,
            pval_threshold=pval_threshold,
        )
    elif variant is not None:
        query = xqtl_queries.XqtlSingleSnpMr.variant.format(
            variant=variant,
            qtl_type=qtl_type.value,
            pval_threshold=pval_threshold,
        )
    response = epigraphdb.run_query(query)
    if qtl_type.value == "pQTL" and len(response["results"]) > 0:
        response = mask_pqtl_snp(response=response, id_list=pqtl_gene_exclude)
    return response


@router.get("/xqtl/single-snp-mr/list")
def get_xqtl_list(
    meta_node: XqtlListMetaNodeInput,
    pval_threshold: float = Query(1e-5, ge=0.0, le=1.0),
    qtl_type: QtlTypeInput = QtlTypeInput.eqtl,
):
    log_args(api="/xqtl/single-snp-mr/list", kwargs=locals())
    if meta_node.value == "GeneGwas":
        query = xqtl_queries.XqtlSingleSnpMrList.gene_gwas.format(
            qtl_type=qtl_type.value, pval_threshold=pval_threshold
        )
    elif meta_node.value == "Gwas":
        query = xqtl_queries.XqtlSingleSnpMrList.gwas.format(
            qtl_type=qtl_type.value, pval_threshold=pval_threshold
        )
    else:
        query = xqtl_queries.XqtlSingleSnpMrList.gene.format(
            qtl_type=qtl_type.value, pval_threshold=pval_threshold
        )
    response = epigraphdb.run_query(query)
    res = (
        pd.json_normalize(response["results"])
        .drop_duplicates()
        .to_dict(orient="records")
    )
    # TODO: formalise this
    res = {"metadata": [], "results": res}
    return res


@router.post("/xqtl/single-snp-mr/gene-by-variant")
def post_xqtl_gene_by_variant(data: GeneByVariantRequest):
    """Get the list of genes associated by an instrument SNP, nested per SNP
    """
    log_args(api="/xqtl/single-snp-mr/gene-by-variant", kwargs=locals())
    query = xqtl_queries.GeneByVariant.query.format(
        variant_list=str(data.variant_list), qtl_type=data.qtl_type
    )
    res = epigraphdb.run_query(query)
    return res


def mask_pqtl_snp(response, id_list: List[str]):
    orig_results = response["results"]
    new_results = [
        item
        for item in orig_results
        if item["gene"]["ensembl_id"] not in id_list
    ]
    res = response
    res["results"] = new_results
    return res

import itertools

import pytest
from starlette.testclient import TestClient

from app.main import app
from app.resources._global import unittest_headers

client = TestClient(app)

multi_snp_mr_url = "/xqtl/multi-snp-mr"
single_snp_mr_url = "/xqtl/single-snp-mr"

exposures = ["ENSG00000187800", None]
outcomes = ["Depressive symptoms", None]
variants = ["rs35422477", None]
mr_methods = ["IVW", "Egger"]
qtl_types = ["eQTL", "pQTL"]
pval_thresholds = [1e-5, 1e-8]

multi_snp_mr_param_list = [
    item
    for item in tuple(
        itertools.product(  # type: ignore
            *[exposures, outcomes, mr_methods, qtl_types, pval_thresholds]
        )
    )
    if item[0] is not None or item[1] is not None
]

single_snp_mr_param_list = [
    item
    for item in tuple(
        itertools.product(  # type: ignore
            *[exposures, outcomes, variants, qtl_types, pval_thresholds]
        )
    )
    if item[0] is not None or item[1] is not None or item[2] is not None
]


@pytest.mark.parametrize(
    "exposure_gene, outcome_trait, mr_method, qtl_type, pval_threshold",
    multi_snp_mr_param_list,
)
def test_multi_snp_mr_exposure_outcome(
    exposure_gene, outcome_trait, mr_method, qtl_type, pval_threshold
):
    payload = {
        "exposure_gene": exposure_gene,
        "outcome_trait": outcome_trait,
        "mr_method": mr_method,
        "qtl_type": qtl_type,
        "pval_threshold": pval_threshold,
    }
    response = client.get(
        multi_snp_mr_url, params=payload, headers=unittest_headers
    )
    assert response.status_code == 200
    assert len(response.json()) >= 1


@pytest.mark.parametrize(
    "exposure_gene, outcome_trait, variant, qtl_type, pval_threshold",
    multi_snp_mr_param_list,
)
def test_single_snp_mr_exposure_outcome(
    exposure_gene, outcome_trait, variant, qtl_type, pval_threshold
):
    payload = {
        "exposure_gene": exposure_gene,
        "outcome_trait": outcome_trait,
        "variant": variant,
        "qtl_type": qtl_type,
        "pval_threshold": pval_threshold,
    }
    response = client.get(
        single_snp_mr_url, params=payload, headers=unittest_headers
    )
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_multi_snp_mr_error():
    payload = {"exposure_gene": None, "outcome_trait": None}
    response = client.get(
        multi_snp_mr_url, params=payload, headers=unittest_headers
    )
    assert response.status_code == 422


def test_single_snp_mr_error():
    payload = {"exposure_gene": None, "outcome_trait": None, "variant": None}
    response = client.get(
        single_snp_mr_url, params=payload, headers=unittest_headers
    )
    assert response.status_code == 422

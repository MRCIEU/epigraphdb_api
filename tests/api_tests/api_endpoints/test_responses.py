import pytest
from loguru import logger
from starlette.testclient import TestClient

from app.apis.status import pqtl_disabled_metrics
from app.apis.status.models import GraphDbMetrics
from app.main import app
from app.models import EpigraphdbGraphs
from app.resources._global import unittest_headers

client = TestClient(app)

response_url_params = [
    # status endpoints
    # /status
    ("/status/ping", None),
    ("/status/api", {"metric": "builds"}),
    *[
        ("/status/db", {"metric": metric, "db": db})
        for db in [item.value for item in EpigraphdbGraphs]
        for metric in [item.value for item in GraphDbMetrics]
        if metric not in pqtl_disabled_metrics and db != "pqtl"
    ],
    # meta nodes
    ("/meta/nodes/list", None),
    ("/meta/nodes/id-name-schema", None),
    ("/meta/nodes/Gwas/list", None),
    ("/meta/nodes/Gwas/list", {"full_data": False}),
    # meta rels
    ("/meta/rels/list", None),
    ("/meta/rels/MR_EVE_MR/list", None),
    ("/meta/api/schema", None),
    ("/meta/api/schema", {"yaml_format": True}),
    # /raw_cypher/
    (
        "/raw_cypher/",
        {"db": "epigraphdb", "query": "MATCH (n) RETURN n LIMIT 2"},
    ),
]

response_url_params_topics = [
    # /confounder
    (
        "/confounder",
        {
            "exposure_trait": "Body mass index",
            "outcome_trait": "Coronary heart disease",
            "type": "confounder",
            "pval_threshold": 1e-5,
        },
    ),
    # /mr
    ("/mr", {"exposure_trait": "Body mass index"}),
    # /obs-cor
    ("/obs-cor", {"trait": "Waist circumference"}),
    ("/obs-cor", {"trait": "Waist circumference", "cor_coef_threshold": 0.2}),
    ("/obs-cor", {"trait": "Waist circumference", "cor_coef_threshold": 0.6}),
    # /genetic-cor
    ("/genetic-cor", {"trait": "Whole body fat mass"}),
    (
        "/genetic-cor",
        {"trait": "Whole body fat mass", "cor_coef_threshold": 0.2},
    ),
    (
        "/genetic-cor",
        {"trait": "Whole body fat mass", "cor_coef_threshold": 0.6},
    ),
    # /ontology
    ("/ontology/gwas-efo", {"efo_term": "systolic blood pressure"}),
    ("/ontology/disease-efo", {"efo_term": "leukemia"}),
    # /drugs/risk-factors
    ("/drugs/risk-factors", {"trait": "Coronary heart disease"}),
    # /pathway
    ("/pathway", {"trait": "LDL cholesterol"}),
    ("/prs", {"trait": "Body mass index"}),
    ("/prs", {"trait": "Body mass index", "pval_threshold": 1e-3}),
    # /pqtl
    (
        "/pqtl/",
        {
            "query": "ADAM19",
            "pvalue": 0.05,
            "searchflag": "proteins",
            "rtype": "simple",
        },
    ),
    # /xqtl/multi-snp-mr
    (
        "/xqtl/multi-snp-mr",
        {
            "exposure_gene": None,
            "outcome_trait": "Depressive symptoms",
            "mr_method": "IVW",
            "qtl_types": "eQTL",
            "pval_threshold": 1e-5,
        },
    ),
    # /xqtl/single-snp-mr
    (
        "/xqtl/single-snp-mr",
        {
            "exposure_gene": None,
            "outcome_trait": "Depressive symptoms",
            "variant": None,
            "qtl_types": "eQTL",
            "pval_threshold": 1e-5,
        },
    ),
]


@pytest.mark.parametrize("url, params", response_url_params)
def test_responses(url, params):
    logger.info(f"url: {url}; params: {params}")
    r = client.get(url, params=params, headers=unittest_headers)
    assert r.raise_for_status() is None


@pytest.mark.parametrize("url, params", response_url_params_topics)
def test_responses_topics(url, params):
    logger.info(f"url: {url}; params: {params}")
    r = client.get(url, params=params, headers=unittest_headers)
    assert r.raise_for_status() is None
    data = r.json()
    assert "results" in data.keys()
    assert len(data["results"]) >= 1

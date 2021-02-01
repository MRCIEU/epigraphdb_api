from pprint import pformat

import pytest
from loguru import logger
from starlette.testclient import TestClient

from app.main import app
from app.resources._global import unittest_headers

client = TestClient(app)

PAYLOADS = {
    "mr_pair": {
        "exposure_trait": "Years of schooling",
        "outcome": "Crohn's disease",
    },
    "mr_exp": {"exposure_trait": "Years of schooling"},
    "mr_outcome": {"outcome_trait": "Years of schooling"},
    "mr_exp_pval": {
        "exposure_trait": "Body mass index",
        "pval_threshold": 1e-8,
    },
}


@pytest.mark.parametrize("key", PAYLOADS.keys())
def test_mr(key):
    payload = PAYLOADS[key]
    r = client.get("/mr", params=payload, headers=unittest_headers)
    assert r.raise_for_status() is None
    data = r.json()
    logger.info(pformat(data))
    assert len(data) >= 1
    assert len(data["results"]) >= 1


class TestMrExceptions:
    def test_none_exposure_outcome(self):
        payload = {"exposure_trait": None, "outcome": None}
        r = client.get("/mr", params=payload, headers=unittest_headers)
        assert r.status_code == 422

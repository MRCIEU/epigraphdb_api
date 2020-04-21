from starlette.testclient import TestClient

from app.main import app
from app.resources._global import unittest_headers

client = TestClient(app)


def test_mr_pair():
    payload = {
        "exposure_trait": "Years of schooling",
        "outcome": "Crohn's disease",
    }
    r = client.get("/mr", params=payload, headers=unittest_headers)
    assert r.status_code == 200 and len(r.json()) >= 1


def test_mr_exp():
    payload = {"exposure_trait": "Years of schooling"}
    r = client.get("/mr", params=payload, headers=unittest_headers)
    assert r.status_code == 200 and len(r.json()) >= 1


def test_mr_outcome():
    payload = {"outcome_trait": "Years of schooling"}
    r = client.get("/mr", params=payload, headers=unittest_headers)
    assert r.status_code == 200 and len(r.json()) >= 1


def test_mr_exp_pval():
    payload = {"exposure_trait": "Body mass index", "pval_threshold": 1e-8}
    r = client.get("/mr", params=payload, headers=unittest_headers)
    assert r.status_code == 200 and len(r.json()) >= 1


class TestMrExceptions:
    def test_none_exposure_outcome(self):
        payload = {"exposure_trait": None, "outcome": None}
        r = client.get("/mr", params=payload, headers=unittest_headers)
        assert r.status_code == 422

import pytest
from starlette.testclient import TestClient

from app.main import app
from app.resources._global import unittest_headers

client = TestClient(app)
url = "/confounder"


@pytest.mark.parametrize(
    "exposure_trait, outcome_trait, type, pval_threshold",
    [
        ("Body mass index", "Coronary heart disease", "confounder", 1e-5),
        ("Body mass index", "Coronary heart disease", "intermediate", 1e-5),
        (
            "Body mass index",
            "Coronary heart disease",
            "reverse_intermediate",
            1e-5,
        ),
        ("Body mass index", "Coronary heart disease", "collider", 1e-5),
    ],
)
def test_confounder(exposure_trait, outcome_trait, type, pval_threshold):
    payload = {
        "exposure_trait": exposure_trait,
        "outcome_trait": outcome_trait,
        "type": type,
        "pval_threshold": pval_threshold,
    }
    response = client.get(url, params=payload, headers=unittest_headers)
    assert response.raise_for_status() is None
    assert len(response.json()) >= 1


class TestConfounderError:
    def test_empty_exposure_outcome(self):
        payload = {
            "exposure_trait": None,
            "outcome_trait": None,
            "type": "confounder",
        }
        response = client.get(url, params=payload, headers=unittest_headers)
        assert response.status_code == 422

    def test_undefined_confounder_type(self):
        payload = {
            "exposure_trait": "Body mass index",
            "outcome_trait": "Coronary heart disease",
            "type": "foobar",
        }
        response = client.get(url, params=payload, headers=unittest_headers)
        assert response.status_code == 422
        assert response.json()["detail"][0]["type"] == "type_error.enum"

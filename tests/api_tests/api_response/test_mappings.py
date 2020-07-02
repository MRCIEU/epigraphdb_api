from starlette.testclient import TestClient

from app.main import app
from app.resources._global import unittest_headers

client = TestClient(app)


def test_by_gene_id_error():
    payload = {
        "by_gene_id": False,
        "gene_id_list": ["ENSG00000162594", "ENSG00000113302"],
    }
    r = client.post(
        url="/mappings/gene-to-protein", json=payload, headers=unittest_headers
    )
    assert r.status_code == 422

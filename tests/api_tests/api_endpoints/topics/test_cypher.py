from starlette.testclient import TestClient

from app.main import app
from app.resources._global import unittest_headers

client = TestClient(app)


def test_cypher_nodes():
    query = """
    MATCH (n) RETURN n LIMIT 20
    """.replace(
        "\n", " "
    )
    payload = {"query": query}
    r = client.post("/cypher", json=payload, headers=unittest_headers)
    assert r.raise_for_status() is None
    assert len(r.json()) >= 1
    assert len(r.json()["results"]) >= 1


def test_cypher_rels():
    query = """
    MATCH p=(n)-[r]-(m) RETURN r LIMIT 20
    """.replace(
        "\n", " "
    )
    payload = {"query": query}
    r = client.post("/cypher", json=payload, headers=unittest_headers)
    assert r.raise_for_status() is None
    assert len(r.json()) >= 1
    assert len(r.json()["results"]) >= 1

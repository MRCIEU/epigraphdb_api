from starlette.testclient import TestClient

from app.main import app
from app.resources._global import unittest_headers
from app.settings import api_key, epigraphdb, pqtl

client = TestClient(app)


def test_raw_cypher():
    payload = {
        "db": "epigraphdb",
        "query": "MATCH (n) RETURN n LIMIT 2",
        "api_key": api_key,
    }
    r = client.get("/raw_cypher/", params=payload, headers=unittest_headers)
    assert r.status_code == 200 and len(r.json()) >= 1


def test_custom_db():
    for neo4j_db in [epigraphdb, pqtl]:
        payload = {
            "query": "MATCH (n) RETURN n LIMIT 2",
            "db": None,
            "hostname": neo4j_db.hostname,
            "bolt_port": neo4j_db.bolt_port,
            "user": neo4j_db.user,
            "password": neo4j_db.password,
            "api_key": api_key,
        }
        r = client.get(
            "/raw_cypher/", params=payload, headers=unittest_headers
        )
        assert r.status_code == 200 and len(r.json()) >= 1

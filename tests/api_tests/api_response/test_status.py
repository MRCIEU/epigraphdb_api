from starlette.testclient import TestClient

from app.main import app
from app.resources._global import unittest_headers

client = TestClient(app)


class TestPing:
    def test_ping(self):
        r = client.get("/status/ping", headers=unittest_headers)
        assert r.status_code == 200 and len(r.json()) >= 1


class TestApiStatus:
    def test_api_builds(self):
        payload = {"metric": "builds"}
        r = client.get("/status/api", params=payload, headers=unittest_headers)
        assert r.status_code == 200 and len(r.json()) >= 1


class TestDbStatus:
    def test_db_get_epigraphdb_count_all_nodes(self):
        payload = {"metric": "count_all_nodes", "db": "epigraphdb"}
        r = client.get("/status/db", params=payload, headers=unittest_headers)
        assert r.status_code == 200 and len(r.json()) >= 1

    def test_db_get_pqtl_count_all_nodes(self):
        payload = {"metric": "count_all_nodes", "db": "pqtl"}
        r = client.get("/status/db", params=payload, headers=unittest_headers)
        assert r.status_code == 200 and len(r.json()) >= 1

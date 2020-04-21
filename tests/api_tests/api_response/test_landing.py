from starlette.testclient import TestClient

from app.main import app
from app.resources._global import unittest_headers

client = TestClient(app)


def test_landing():
    r = client.get("/", headers=unittest_headers)
    assert r.status_code == 200

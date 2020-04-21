from starlette.testclient import TestClient

from app.main import app
from app.resources._global import unittest_headers

client = TestClient(app)


def test_obs_cor():
    payload = {"trait": "Body mass index"}
    r = client.get("/obs-cor", params=payload, headers=unittest_headers)
    assert r.status_code == 200 and len(r.json()) >= 1

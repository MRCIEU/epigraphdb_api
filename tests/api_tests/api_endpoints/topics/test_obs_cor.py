from pprint import pformat

from loguru import logger
from starlette.testclient import TestClient

from app.main import app
from app.resources._global import unittest_headers

client = TestClient(app)


def test_obs_cor():
    payload = {"trait": "Body mass index (BMI)"}
    r = client.get("/obs-cor", params=payload, headers=unittest_headers)
    assert r.raise_for_status() is None
    data = r.json()
    logger.info(pformat(data))
    assert len(r.json()["results"]) > 0

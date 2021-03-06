from pprint import pformat

import pytest
from loguru import logger
from starlette.testclient import TestClient

from app.main import app
from app.resources._global import unittest_headers
from app.resources.public_endpoints import topic_params, util_params

client = TestClient(app)


@pytest.mark.parametrize("endpoint", topic_params.keys())
def test_topic_endpoints(endpoint):
    tests = topic_params[endpoint]["tests"]
    for test in tests:
        if "endpoint" in test.keys():
            actual_endpoint = test["endpoint"]
        else:
            actual_endpoint = endpoint
        method, route = actual_endpoint.split(" ")
        params = test["params"]
        if method == "GET":
            r = client.get(url=route, params=params, headers=unittest_headers)
            assert r.raise_for_status() is None
        elif method == "POST":
            r = client.post(url=route, json=params, headers=unittest_headers)
            assert r.raise_for_status() is None
        data = r.json()
        logger.info(pformat(data))
        assert "results" in data.keys()
        assert len(data["results"]) > 0


@pytest.mark.parametrize("endpoint", util_params.keys())
def test_util_endpoints(endpoint):
    tests = util_params[endpoint]["tests"]
    for test in tests:
        if "endpoint" in test.keys():
            actual_endpoint = test["endpoint"]
        else:
            actual_endpoint = endpoint
        method, route = actual_endpoint.split(" ")
        params = test["params"]
        if method == "GET":
            r = client.get(url=route, params=params, headers=unittest_headers)
            assert r.raise_for_status() is None
        elif method == "POST":
            r = client.post(url=route, json=params, headers=unittest_headers)
            assert r.raise_for_status() is None

import pytest
from starlette.testclient import TestClient

from app.main import app
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
            r = client.get(url=route, params=params)
            assert r.status_code == 200
        elif method == "POST":
            r = client.post(url=route, json=params)
            assert r.status_code == 200
        data = r.json()
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
            r = client.get(url=route, params=params)
            assert r.status_code == 200
        elif method == "POST":
            r = client.post(url=route, json=params)
            assert r.status_code == 200

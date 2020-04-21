from typing import Dict

import pytest
from starlette.testclient import TestClient

from app.apis.pqtl import ListFlagInput, PrflagInput, RtypeInput
from app.main import app
from app.resources._global import unittest_headers

client = TestClient(app)

params_pqtl = [
    # /pqtl/, proteins
    *[
        (
            "/pqtl/",
            {
                "query": "ADAM19",
                "pvalue": 0.05,
                "searchflag": "proteins",
                "rtype": rtype,
            },
        )
        for rtype in [item.value for item in RtypeInput]
    ],
    # /pqtl/, traits
    *[
        (
            "/pqtl/",
            {
                "query": "Inflammatory bowel disease",
                "pvalue": 0.05,
                "searchflag": "traits",
                "rtype": rtype,
            },
        )
        for rtype in [item.value for item in RtypeInput]
    ],
    # /pqtl/pleio
    *[
        ("/pqtl/pleio/", {"rsid": "rs1926447", "prflag": prflag})
        for prflag in [item.value for item in PrflagInput]
    ],
    # /pqtl/list/
    *[
        ("/pqtl/list", {"flag": flag})
        for flag in [item.value for item in ListFlagInput]
    ],
]


@pytest.mark.parametrize("url, params", params_pqtl)
def test_pqtl(url: str, params: Dict[str, object]):
    response = client.get(url, params=params, headers=unittest_headers)
    assert response.status_code == 200
    if isinstance(response.json()["results"], list):
        assert len(response.json()["results"]) > 0
    else:
        assert response.json()["results"] is not None

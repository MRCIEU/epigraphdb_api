from pprint import pformat

import pytest
from loguru import logger
from starlette.testclient import TestClient

from app.main import app
from app.models.schema_meta_nodes import meta_node_schema
from app.models.schema_meta_rels import meta_path_schema
from app.resources._global import unittest_headers

client = TestClient(app)


def test_get_schema():
    url = "/meta/schema"
    response = client.get(url, headers=unittest_headers)
    assert response.raise_for_status() is None


@pytest.mark.parametrize("path", ["/meta/nodes/list", "/meta/rels/list"])
def test_get_meta(path):
    response = client.get(path, headers=unittest_headers)
    assert response.raise_for_status() is None
    assert len(response.json()) >= 1


@pytest.mark.parametrize("meta_node", meta_node_schema.keys())
def test_get_meta_nodes(meta_node):
    url = f"/meta/nodes/{meta_node}/list"
    # full data
    response = client.get(url, headers=unittest_headers)
    assert response.raise_for_status() is None
    data = response.json()
    logger.info(pformat(data))
    assert len(data) >= 1
    # id and name
    response = client.get(
        url, params={"full_data": False, "limit": 10}, headers=unittest_headers
    )
    assert response.raise_for_status() is None
    assert len(response.json()) >= 1
    assert len(data["results"]) >= 1


@pytest.mark.parametrize("meta_rel", meta_path_schema.keys())
def test_get_meta_rels(meta_rel):
    url = f"/meta/rels/{meta_rel}/list"
    response = client.get(url, headers=unittest_headers)
    data = response.json()
    logger.info(pformat(data))
    assert response.raise_for_status() is None
    assert len(data) >= 1
    assert len(data["results"]) >= 1


@pytest.mark.parametrize(
    "meta_node, id, name",
    [
        ("Disease", "influenza", None),
        ("Disease", None, "influenza"),
        ("Drug", "CODEINE", None),
        ("Drug", None, "CODEINE"),
        ("Efo", "http://www.orpha.net/ORDO/Orphanet_171866", None),
        ("Efo", None, "pathological myopia"),
        ("Gene", "ENSG00000232163", None),
        ("Gene", None, "RPLP1P13"),
        ("Tissue", "Adrenal Gland", None),
        ("Tissue", None, "Adrenal Gland"),
        ("Gwas", "2", None),
        ("Gwas", None, "Body mass index"),
        ("Gwas", "1239", None),
        ("Gwas", None, "Years of schooling"),
        ("Literature", "22479202", None),
        ("Literature", None, "22479202"),
        ("Pathway", "R-HSA-68689", None),
        ("Pathway", None, "CDC6 association with the ORC:origin complex"),
        ("Protein", "A6NJS3", None),
        ("Protein", None, "A6NJS3"),
        ("LiteratureTerm", "C0752046", None),
        ("LiteratureTerm", None, "Single Nucleotide Polymorphism"),
        ("Variant", "rs1347572", None),
        ("Variant", None, "rs1347572"),
    ],
)
def test_get_nodes_search(meta_node, id, name):
    url = f"/meta/nodes/{meta_node}/search"
    payload = {"meta_node": meta_node, "id": id, "name": name}
    response = client.get(url, params=payload, headers=unittest_headers)
    assert response.raise_for_status() is None
    assert len(response.json()) >= 1


@pytest.mark.parametrize(
    "meta_node, id, name, limit, full_data",
    [
        item
        for nested_item in [
            *[
                [
                    ("Gene", "ENSG00000232163", None, limit, full),
                    ("Gene", None, "RPLP1P13", limit, full),
                    ("Tissue", "Adrenal Gland", None, limit, full),
                    ("Tissue", None, "Adrenal Gland", limit, full),
                    ("Gwas", "2", None, limit, full),
                    ("Gwas", None, "Body mass index", limit, full),
                    ("Gwas", "1239", None, limit, full),
                    ("Gwas", None, "Years of schooling", limit, full),
                    ("Literature", "22479202", None, limit, full),
                    ("Literature", None, "22479202", limit, full),
                ]
                for limit in [3, 5, 10]
                for full in [True, False]
            ]
        ]
        for item in nested_item
    ],
)
def test_get_nodes_search_more_params(meta_node, id, name, limit, full_data):
    url = f"/meta/nodes/{meta_node}/search"
    payload = {
        "meta_node": meta_node,
        "id": id,
        "name": name,
        "limit": limit,
        "full_data": full_data,
    }
    response = client.get(url, params=payload, headers=unittest_headers)
    assert response.raise_for_status() is None
    data = response.json()
    assert len(data) >= 1


@pytest.mark.parametrize(
    "meta_node_source, id_source, meta_node_target,"
    + " id_target, max_path_length, limit",
    [
        ("Gwas", "1", "Gwas", "361", 1, 2),
        ("Variant", "rs10781543", "Gwas", "12", 1, 2),
    ],
)
def test_get_paths_search(
    meta_node_source,
    id_source,
    meta_node_target,
    id_target,
    max_path_length,
    limit,
):
    url = "/meta/paths/search"
    params = {
        "meta_node_source": meta_node_source,
        "id_source": id_source,
        "meta_node_target": meta_node_target,
        "id_target": id_target,
        "max_path_length": max_path_length,
        "limit": limit,
    }
    response = client.get(url, params=params, headers=unittest_headers)
    assert response.raise_for_status() is None

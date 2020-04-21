import pytest
from loguru import logger

from app.models.schema_meta_nodes import meta_node_schema
from app.models.schema_meta_rels import meta_path_schema, meta_rel_schema
from app.settings import epigraphdb


def test_meta_node_name():
    query = """
        MATCH (n) RETURN DISTINCT labels(n)[0] as label
    """
    res = set([_["label"] for _ in epigraphdb.run_query(query)["results"]])
    expected_res = set([_ for _ in meta_node_schema.keys()])
    assert res == expected_res


def test_meta_rel_name():
    query = """
        MATCH (n)-[r]-(m) RETURN DISTINCT type(r) as label
    """
    res = set([_["label"] for _ in epigraphdb.run_query(query)["results"]])
    expected_res = set([_ for _ in meta_rel_schema.keys()])
    assert res == expected_res


@pytest.mark.parametrize("meta_node_name", list(meta_node_schema.keys()))
def test_meta_node_schema(meta_node_name):
    schema_model = meta_node_schema[meta_node_name]
    query = """
        MATCH (n: {meta_node_name})
        WITH n, rand() AS index
        RETURN n
        ORDER BY index
        LIMIT 1000
    """.format(
        meta_node_name=meta_node_name
    )
    res = epigraphdb.run_query(query)["results"]
    for item in res:
        # if None => black list
        if schema_model is not None:
            node = schema_model(**item["n"])
            assert isinstance(node, schema_model)


@pytest.mark.parametrize("meta_rel_name", list(meta_rel_schema.keys()))
def test_meta_rel_schema(meta_rel_name):
    schema_model = meta_rel_schema[meta_rel_name]
    query = """
        MATCH p=(n)-[r: {meta_rel_name}]-(m)
        WITH n, r, m, rand() AS index
        RETURN r
        ORDER BY index
        LIMIT 1000
    """.format(
        meta_rel_name=meta_rel_name
    )
    res = epigraphdb.run_query(query)["results"]
    for item in res:
        rel = schema_model(**item["r"])
        assert isinstance(rel, schema_model)


@pytest.mark.parametrize(
    "meta_rel_name", [key for key in meta_rel_schema.keys()]
)
def test_meta_path_schema(meta_rel_name):
    meta_path = meta_path_schema[meta_rel_name]
    expected_source_node = meta_path[0]
    expected_target_node = meta_path[1]
    query = """
        MATCH p=(source_node)-[r: {meta_rel_name}]->(target_node)
        WITH
            labels(source_node)[0] AS source_node,
            labels(target_node)[0] AS target_node,
            rand() AS index
        RETURN
            source_node, target_node
        ORDER BY index
        LIMIT 500
    """.format(
        meta_rel_name=meta_rel_name
    )
    res = epigraphdb.run_query(query)["results"]
    source_nodes = list(set([_["source_node"] for _ in res]))
    target_nodes = list(set([_["target_node"] for _ in res]))
    logger.info([source_nodes, expected_source_node])
    logger.info([target_nodes, expected_target_node])
    assert len(source_nodes) == 1
    assert len(target_nodes) == 1
    assert source_nodes[0] == expected_source_node
    assert target_nodes[0] == expected_target_node

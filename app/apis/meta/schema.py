from typing import Dict, List, Optional

import pandas as pd
from graphviz import Digraph
from typing_extensions import TypedDict

from app.apis.status import get_db_metric
from app.apis.status.models import GraphDbMetrics
from app.models import EpigraphdbGraphs
from app.settings import cache_dir
from app.utils.cache import cache_func_call_json

schema_ignore_nodes = ["Meta"]


class MetaSchemaNodeProperty(TypedDict):
    type: str
    indexed: bool
    unique: bool


class MetaSchemaEdgeProperty(TypedDict):
    array: bool
    type: str


class MetaSchemaNode(TypedDict):
    count: int
    properties: Dict[str, MetaSchemaNodeProperty]


class MetaSchemaEdge(TypedDict):
    count: int
    properties: Optional[Dict[str, MetaSchemaEdgeProperty]]


class MetaSchemaConnection(TypedDict):
    rel: str
    from_node: str
    to_node: str
    count: int


class MetaSchemaData(TypedDict):
    nodes: Dict[str, MetaSchemaNode]
    edges: Dict[str, MetaSchemaEdge]
    connections: List[MetaSchemaConnection]


def generate_schema(overwrite: bool = False) -> MetaSchemaData:
    schema = cache_func_call_json(
        cache_name="schema",
        func=process_schema,
        params={"overwrite": overwrite},
        overwrite=overwrite,
    )
    return schema


def process_schema(overwrite: bool = False) -> MetaSchemaData:
    db_schema_data = cache_func_call_json(
        cache_name="schema_raw",
        func=schema_request,
        params=None,
        overwrite=overwrite,
    )
    db_meta_node_count_data = cache_func_call_json(
        cache_name="db_meta_node_count",
        func=meta_node_count_request,
        params=None,
        overwrite=overwrite,
    )
    db_meta_rel_count_data = cache_func_call_json(
        cache_name="db_meta_rel_count",
        func=meta_rel_count_request,
        params=None,
        overwrite=overwrite,
    )
    nodes_data: Dict[str, MetaSchemaNode] = process_nodes(
        schema_data=db_schema_data,
        node_count=db_meta_node_count_data,
        ignore_nodes=schema_ignore_nodes,
    )
    edges_data: Dict[str, MetaSchemaEdge] = process_edges(db_schema_data)
    connections_data: List[MetaSchemaConnection] = process_connections(
        db_schema_data,
        edges_data,
        edge_count=db_meta_rel_count_data,
        ignore_nodes=schema_ignore_nodes,
    )
    res: MetaSchemaData = {
        "nodes": nodes_data,
        "edges": edges_data,
        "connections": connections_data,
    }
    return res


def schema_request():
    data = get_db_metric(
        metric=GraphDbMetrics.schema, db=EpigraphdbGraphs.epigraphdb
    )[0]["value"]
    return data


def meta_node_count_request():
    data = get_db_metric(
        metric=GraphDbMetrics.count_nodes_by_label,
        db=EpigraphdbGraphs.epigraphdb,
    )
    data = {_["node_name"][0]: _["count"] for _ in data}
    return data


def meta_rel_count_request():
    data = get_db_metric(
        metric=GraphDbMetrics.count_rels_by_type,
        db=EpigraphdbGraphs.epigraphdb,
    )
    data = {_["relationshipType"]: _["count"] for _ in data}
    return data


def process_nodes(
    schema_data, node_count, ignore_nodes: List[str]
) -> Dict[str, MetaSchemaNode]:
    def pick_node_items(node_value, node_name) -> MetaSchemaNode:
        items: MetaSchemaNode = {
            "count": node_count[node_name],
            "properties": {
                prop_key: {
                    "type": prop_val["type"],
                    "indexed": prop_val["indexed"],
                    "unique": prop_val["unique"],
                }
                for prop_key, prop_val in node_value["properties"].items()
            },
        }
        return items

    nodes_data = {
        key: pick_node_items(value, key)
        for key, value in schema_data.items()
        if value["type"] == "node" and key not in ignore_nodes
    }
    return nodes_data


def process_edges(schema_data) -> Dict[str, MetaSchemaEdge]:
    def pick_edges_items(edge):
        if edge["properties"] != {}:
            props = pick_edges_props(edge["properties"])
        else:
            props = None
        items = {"count": edge["count"], "properties": props}
        return items

    def pick_edges_props(props):
        res = {
            prop_key: {"array": prop_val["array"], "type": prop_val["type"]}
            for prop_key, prop_val in props.items()
        }
        return res

    edges_data = {
        key: pick_edges_items(value)
        for key, value in schema_data.items()
        if value["type"] == "relationship"
    }
    return edges_data


def process_connections(
    schema_data, edges_data, edge_count, ignore_nodes: List[str]
) -> List[MetaSchemaConnection]:
    connections_nodes = {
        key: value["relationships"]
        for key, value in schema_data.items()
        if value["type"] == "node" and key not in ignore_nodes
    }
    connections_data = pd.concat(
        [
            pd.concat(
                [
                    pd.DataFrame(
                        {
                            "rel": [node_rel_key],
                            "from_node": [
                                node_name
                                if node_rel_value["direction"] == "out"
                                else node_rel_value["labels"][0]
                            ],
                            "to_node": [
                                node_name
                                if node_rel_value["direction"] == "in"
                                else node_rel_value["labels"][0]
                            ],
                        }
                    )
                    for node_rel_key, node_rel_value in node_rels.items()
                ]
            )
            for node_name, node_rels in connections_nodes.items()
        ]
    )
    edges_df = pd.DataFrame.from_dict(
        {key: {"count": edge_count[key]} for key, value in edges_data.items()},
        orient="index",
    )
    connections_data = (
        connections_data.drop_duplicates()
        .reset_index(drop=True)
        # Add count
        # NOTE: this assumes meta rels are unique to meta nodes
        .merge(edges_df, left_on="rel", right_index=True)
        .to_dict(orient="records")
    )
    return connections_data


def render_schema_graphviz(schema):
    dot = Digraph(
        name="EpiGraphDB schema",
        node_attr={"shape": "record"},
        graph_attr={"rankdir": "LR"},
    )
    for node_name, node_value in schema["nodes"].items():
        if node_value["properties"] is not None:
            props = " | " + " | ".join(
                [
                    "{prop_name}: {type} {index} {unique}".format(
                        prop_name=prop_name,
                        type=prop_value["type"],
                        index="indexed" if prop_value["indexed"] else "",
                        unique="unique" if prop_value["unique"] else "",
                    )
                    for prop_name, prop_value in node_value[
                        "properties"
                    ].items()
                ]
            )
        else:
            props = ""
        label = "< <B> {name} {count:,} </B> {props} >".format(
            name=node_name, count=node_value["count"], props=props
        )
        dot.node(name=node_name, label=label)
    for connection in schema["connections"]:
        label = "< <B> {name} </B> <BR/> {count:,} >".format(
            name=connection["rel"], count=connection["count"]
        )
        dot.edge(
            tail_name=connection["from_node"],
            head_name=connection["to_node"],
            label=label,
        )
    return dot


def render_graphviz(dot, overwrite: bool = False):
    cache_file = cache_dir / "epigraphdb-schema.png"
    if not cache_file.exists() or overwrite:
        dot.render(
            format="png", filename="epigraphdb-schema", directory=cache_dir
        )
    return cache_file

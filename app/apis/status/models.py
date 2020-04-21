from enum import Enum

from pydantic import BaseModel


class GraphDbMetrics(str, Enum):
    count_all_nodes = "count_all_nodes"
    count_all_rels = "count_all_rels"
    count_meta_nodes = "count_meta_nodes"
    count_meta_rels = "count_meta_rels"
    list_node_labels = "list_node_labels"
    list_rel_types = "list_rel_types"
    describe_nodes = "describe_nodes"
    count_nodes_by_label = "count_nodes_by_label"
    count_rels_by_type = "count_rels_by_type"
    schema = "schema"
    graph_metadata = "graph_metadata"


class PingResponse(BaseModel):
    """Response from /ping for an underlying service component."""

    name: str
    url: str
    available: bool

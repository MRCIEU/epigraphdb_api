from typing import Optional

from app.models.schema_meta_nodes import meta_node_id_name_mappings

from .queries import (
    full_node_data_fragment,
    search_node_by_id_template,
    search_node_by_name_template,
    search_node_neighbour_by_id_template,
    search_path_template,
    simple_node_data_fragment,
)


def nodes_search_query_builder(
    meta_node: str,
    id: Optional[str],
    name: Optional[str],
    limit: int = 10,
    full_data: bool = True,
) -> str:
    """Returns the query for the search."""
    name_field = meta_node_id_name_mappings[meta_node]["name"]
    id_field = meta_node_id_name_mappings[meta_node]["id"]
    if full_data:
        node_data_field = full_node_data_fragment
    else:
        node_data_field = simple_node_data_fragment.format(
            id_field=id_field, name_field=name_field
        )
    if name is not None:
        query = search_node_by_name_template.format(
            meta_node=meta_node,
            name_field=name_field,
            name_query=name,
            node_data_field=node_data_field,
            limit=limit,
        )
        return query
    elif id is not None:
        query = search_node_by_id_template.format(
            meta_node=meta_node,
            id_field=id_field,
            id_query=id,
            node_data_field=node_data_field,
            limit=limit,
        )
        return query
    else:
        return ""


def nodes_neighbour_query_builder(
    meta_node: str, id: Optional[str], limit: int = 50
) -> str:
    """Query builder for searching neighbours of a node"""
    id_field = meta_node_id_name_mappings[meta_node]["id"]
    query = search_node_neighbour_by_id_template.format(
        meta_node=meta_node, id_field=id_field, id_query=id, limit=limit
    )
    return query


def paths_search_query_builder(
    meta_node_source: str,
    id_source: str,
    meta_node_target: str,
    id_target: str,
    max_path_length: int = 3,
    limit: int = 100,
) -> str:
    id_field_source = meta_node_id_name_mappings[meta_node_source]["id"]
    id_field_target = meta_node_id_name_mappings[meta_node_target]["id"]
    query = search_path_template.format(
        meta_node_source=meta_node_source,
        meta_node_target=meta_node_target,
        id_field_source=id_field_source,
        id_field_target=id_field_target,
        id_source=id_source,
        id_target=id_target,
        max_path_length=max_path_length,
        limit=limit,
    )
    return query

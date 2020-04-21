full_node_data_fragment = "node"

simple_node_data_fragment = (
    "id(node) AS _id, node.{id_field} AS id, node.{name_field} AS name"
)

search_node_by_name_template = """
    MATCH
        (node: {meta_node})
    WHERE
        node.{name_field} =~ "(?i).*{name_query}.*"
    RETURN {node_data_field}
    LIMIT {limit};
"""


search_node_by_id_template = """
    MATCH
        (node: {meta_node} {{{id_field}: "{id_query}"}})
    RETURN {node_data_field}
    LIMIT {limit};
"""


search_node_neighbour_by_id_template = """
    MATCH
        (neighbour)-[rel]-(node: {meta_node} {{{id_field}: "{id_query}"}})
    WITH neighbour, rel, node,
    CASE
        WHEN LABELS(neighbour)[0] = "Gwas"
    THEN
    {{
        meta_node: LABELS(neighbour)[0],
        meta_rel: TYPE(rel),
        node_data: neighbour {{.id, .trait}}
    }}
    ELSE
    {{
        meta_node: LABELS(neighbour)[0],
        meta_rel: TYPE(rel),
        node_data: neighbour
    }}
    END
    AS neighbour_data
    RETURN
    {{
        meta_node: LABELS(node)[0],
        id: node.{id_field},
        neighbour: collect(neighbour_data)[0..({limit}-1)]
    }} AS data
"""


search_path_template = """
    MATCH
        p=(n:{meta_node_source} {{{id_field_source}: "{id_source}"}})
          -[*1..{max_path_length}]-
          (m:{meta_node_target} {{{id_field_target}: "{id_target}"}})
    WITH nodes(p) AS node_list, relationships(p) AS rel_list
    RETURN
    [
        x in node_list |
        {{
            _id: id(x),
            meta_node: labels(x)[0],
            node_value: x
        }}
    ] AS node_data,
    [
        i in range(0, size(rel_list) - 1) |
        {{
            meta_rel: type(rel_list[i]),
            rel_index: i,
            rel__id: id(rel_list[i]),
            rel_value: rel_list[i],
            head_meta_node: labels(startNode(rel_list[i]))[0],
            head_node__id: id(startNode(rel_list[i])),
            end_meta_node: labels(endNode(rel_list[i]))[0],
            end_node__id: id(endNode(rel_list[i]))
        }}
    ] AS rel_data
    LIMIT {limit};
"""


class MetaQueries:
    """Metagraph queries"""

    list_node_labels = "CALL db.labels()"

    list_rel_types = "CALL db.relationshipTypes()"

    get_nodes = """
    MATCH
        (n:{meta_node})
    RETURN
        n
    SKIP {skip}
    LIMIT {limit}
    """.replace(
        "\n", " "
    )

    get_rels = """
    MATCH
        (n)-[r: {meta_rel}]-(m)
    RETURN
        n, r, m
    SKIP {skip}
    LIMIT {limit}
    """.replace(
        "\n", " "
    )

    get_node_id_and_name_fields = """
    MATCH
        (n:{meta_node})
    RETURN
        n.{id_field} AS id,
        n.{name_field} AS name
    SKIP {offset}
    LIMIT {limit}
    """.replace(
        "\n", " "
    )

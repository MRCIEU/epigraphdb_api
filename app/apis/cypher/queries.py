class CypherBuilder:
    query = """
        MATCH
            (source_node:{source_meta_node})
            -[rel:{meta_rel}]-
            (target_node:{target_meta_node})
        {where}
        RETURN
            source_node,
            rel,
            target_node
        {order_by}
        LIMIT {limit}
    """

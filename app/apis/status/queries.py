class DbStatusQueries:
    """Cypher scripts related to data profiling"""

    count_all_nodes = "MATCH (n) RETURN count(n) as num_nodes"

    count_all_rels = "MATCH ()-->() RETURN count(*)"

    count_meta_rels = """
    CALL
        db.relationshipTypes()
    YIELD
        relationshipType
    RETURN
        count(relationshipType) AS n
    """.replace(
        "\n", " "
    )

    count_meta_nodes = """
    CALL
        db.labels()
    YIELD
        label
    RETURN
        count(label) AS n
    """.replace(
        "\n", " "
    )

    list_node_labels = "CALL db.labels()"

    list_rel_types = "CALL db.relationshipTypes()"

    # What kind of nodes exist
    # Sample some nodes, reporting on property and relationship counts
    # per node.
    describe_nodes = """
    MATCH (n) WHERE rand() <= 0.1
    RETURN
        DISTINCT labels(n),
        count(*) AS SampleSize,
        avg(size(keys(n))) as Avg_PropertyCount,
        min(size(keys(n))) as Min_PropertyCount,
        max(size(keys(n))) as Max_PropertyCount,
        avg(size( (n)-[]-() ) ) as Avg_RelationshipCount,
        min(size( (n)-[]-() ) ) as Min_RelationshipCount,
        max(size( (n)-[]-() ) ) as Max_RelationshipCount
    """.replace(
        "\n", " "
    )

    # What is related, and how
    schema = "CALL apoc.meta.schema"

    # Count nodes by label
    count_nodes_by_label = """
    MATCH (n)
    RETURN DISTINCT
        labels(n) as node_name,
        count(labels(n)) as count
    """

    # Count rels by type
    count_rels_by_type = """
    MATCH p=()-[r]->()
    RETURN DISTINCT
        type(r) as relationshipType,
        count(type(r)) as count
    """

    graph_metadata = """
    MATCH (n:Meta) RETURN n as meta_data
    """

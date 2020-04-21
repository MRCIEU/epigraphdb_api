from app.utils.process_query import format_response, trim_cypher_query


def test_format_response():
    query = """
    Some
        cypher
    query
    """
    data = [
        {"res0_key": ["res0_values"]},
        {"res1_0_key": ["res1_0_values"], "res1_1_key": ["res1_1_values"]},
        {"res2_key": ["res2_values"]},
    ]

    expected_response = {
        "metadata": {
            "query": "Some cypher query",
            "empty_results": False,
            "total_seconds": None,
        },
        "results": [
            {"res0_key": ["res0_values"]},
            {"res1_0_key": ["res1_0_values"], "res1_1_key": ["res1_1_values"]},
            {"res2_key": ["res2_values"]},
        ],
    }
    response = format_response(data=data, query=query)
    assert response == expected_response


def test_trim_cypher_query():
    query = """
    This is
        a cypher query
    formatted
        for better
    readability
    """.replace(
        "\n", " "
    )
    expected_result = "This is a cypher query formatted for better readability"
    result = trim_cypher_query(query)
    assert result == expected_result

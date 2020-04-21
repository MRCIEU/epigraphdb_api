from app.utils import cypher_fuzzify


def test_cypher_fuzzify():
    input = "Body MasS INdeX"
    expected_res = "(?i).*body mass index.*"
    res = cypher_fuzzify(input)
    assert res == expected_res

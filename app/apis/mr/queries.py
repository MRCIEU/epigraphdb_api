class MRQueries:
    _tail = """
        AND
            mr.pval < {pval_threshold}
        RETURN
            exposure {{.id, .trait}},
            outcome {{.id, .trait}},
            mr {{.b, .se, .pval, .method, .selection, .moescore}}
        ORDER BY mr.pval
        ;
    """
    _head = """
        MATCH
            (exposure:Gwas)-[mr:MR]->(outcome:Gwas)
    """
    pair = (
        _head
        + """
    WHERE
        exposure.trait = "{exposure_trait}"
        AND
        outcome.trait = "{outcome_trait}"
    """
        + _tail
    ).replace("\n", " ")

    exp = (
        _head
        + """
    WHERE
        exposure.trait = "{exposure_trait}"
    """
        + _tail
    ).replace("\n", " ")

    out = (
        _head
        + """
    WHERE
        outcome.trait = "{outcome_trait}"
    """
        + _tail
    ).replace("\n", " ")

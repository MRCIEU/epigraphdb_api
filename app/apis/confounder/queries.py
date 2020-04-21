class ConfounderQueries:
    _tail = """
    WHERE
        r1.pval < {pval_threshold} AND
        r2.pval < {pval_threshold} AND
        r3.pval < {pval_threshold} AND
        cf.id <> exposure.id AND
        cf.id <> outcome.id AND
        exposure.id <> outcome.id AND
        cf.trait <> exposure.trait AND
        cf.trait <> outcome.trait AND
        exposure.trait <> outcome.trait
    RETURN
        exposure {{.id, .trait}},
        outcome {{.id, .trait}},
        cf {{.id, .trait}},
        r1 {{.b, .se, .pval, .selection, .method, .moescore}},
        r2 {{.b, .se, .pval, .selection, .method, .moescore}},
        r3 {{.b, .se, .pval, .selection, .method, .moescore}}
    ORDER BY r1.p;
    """
    confounder = (
        """
        MATCH
            (cf:Gwas)-[r1:MR]->
            (exposure:Gwas {{trait: "{exposure_trait}"}})
            -[r2:MR]->(outcome:Gwas {{trait: "{outcome_trait}"}})
            <-[r3:MR]-(cf:Gwas)
        """
        + _tail
    )
    intermediate = (
        """
        MATCH
            (cf:Gwas)<-[r1:MR]-
            (exposure:Gwas {{trait: "{exposure_trait}"}})
            -[r2:MR]->(outcome:Gwas {{trait: "{outcome_trait}"}})
            <-[r3:MR]-(cf:Gwas)
        """
        + _tail
    )
    reverse_intermediate = (
        """
        MATCH
            (cf:Gwas)-[r1:MR]->
            (exposure:Gwas {{trait: "{exposure_trait}"}})
            -[r2:MR]->(outcome:Gwas {{trait: "{outcome_trait}"}})
            -[r3:MR]->(cf:Gwas)
        """
        + _tail
    )
    collider = (
        """
        MATCH
            (cf:Gwas)<-[r1:MR]-
            (exposure:Gwas {{trait: "{exposure_trait}"}})
            -[r2:MR]->(outcome:Gwas {{trait: "{outcome_trait}"}})
            -[r3:MR]->(cf:Gwas)
        """
        + _tail
    )

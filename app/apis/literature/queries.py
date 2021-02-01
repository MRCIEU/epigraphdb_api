class GwasPairwise:
    _head = """
        MATCH
            (gwas:Gwas)-[gs1:GWAS_TO_LITERATURE_TRIPLE]->(s1:LiteratureTriple)
            -[:SEMMEDDB_OBJ]->(st:LiteratureTerm)<-[:SEMMEDDB_SUB]-
            (s2:LiteratureTriple)<-[gs2:GWAS_TO_LITERATURE_TRIPLE]-(assoc_gwas:Gwas)
        WHERE
    """
    _where = """
        AND
        gs1.pval < {pval_threshold} AND
        gs2.pval < {pval_threshold} AND
        {semmantic_type_query}
    """
    _tail = """
        RETURN
            gwas {{.id, .trait}},
            gs1 {{.pval, .localCount}},
            s1 {{.id, .subject_id, .object_id, .predicate}},
            st {{.name, .type}},
            s2 {{.id, .subject_id, .object_id, .predicate}},
            gs2 {{.pval, .localCount}},
            assoc_gwas {{.id, .trait}}
        SKIP {skip}
        LIMIT {limit}
    """
    trait = (
        _head
        + """
        gwas.trait {eq_symbol} "{trait}"
        """
        + _where
        + _tail
    )
    trait_assoc_trait = (
        _head
        + """
        gwas.trait {eq_symbol} "{trait}" AND
        assoc_gwas.trait {eq_symbol} "{assoc_trait}"
        """
        + _where
        + _tail
    )
    id = (
        _head
        + """
        gwas.id = "{gwas_id}"
        """
        + _where
        + _tail
    )
    id_assoc_id = (
        _head
        + """
        gwas.id = "{gwas_id}" AND
        assoc_gwas.id = "{assoc_gwas_id}"
        """
        + _where
        + _tail
    )


class Gwas:
    _head = """
        MATCH
            (gwas:Gwas)-[gs:GWAS_TO_LITERATURE_TRIPLE]->(triple:LiteratureTriple)
            -[sl:SEMMEDDB_TO_LIT]->(lit:Literature)
        WHERE
    """
    _where = """
        AND
            gs.pval < {pval_threshold}
            {semmed_predicates_clause}
        WITH
            gwas, triple, lit, gs
        MATCH
            (gwas)-[gl:GWAS_TO_LITERATURE]-(lit)
    """
    _tail = """
        RETURN
            gwas {{.id, .trait}},
            gs {{.pval, .localCount}},
            triple {{.id, .predicate}},
            lit {{.id}}
        SKIP {skip}
        LIMIT {limit}
    """
    id = (
        _head
        + """
        gwas.id = "{gwas_id}"
        """
        + _where
        + _tail
    )
    trait = (
        _head
        + """
        gwas.trait {eq_symbol} "{trait}"
        """
        + _where
        + _tail
    )
    id_triple = (
        _head
        + """
        gwas.id = "{gwas_id}" AND
        triple.name = "{semmed_triple_name}"
        """
        + _where
        + _tail
    )
    trait_triple = (
        _head
        + """
        gwas.trait {eq_symbol} "{trait}" AND
        triple.name = "{semmed_triple_name}"
        """
        + _where
        + _tail
    )

class GwasPairwise:
    _head = """
        MATCH
            (gwas:Gwas)-[gs1:GWAS_SEM]->(s1:SemmedTriple)
            -[:SEM_OBJ]->(st:SemmedTerm)<-[:SEM_SUB]-
            (s2:SemmedTriple)<-[gs2:GWAS_SEM]-(assoc_gwas:Gwas)
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
            s1 {{.id, .subject_name, .object_name, .predicate}},
            st {{.name, .type}},
            s2 {{.id, .subject_name, .object_name, .predicate}},
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
            (gwas:Gwas)-[gs:GWAS_SEM]->(triple:SemmedTriple)
            -[sl:SEM_TO_LIT]->(lit:Literature)
        WHERE
    """
    _where = """
        AND
            gs.pval < {pval_threshold}
            {semmed_predicates_clause}
        WITH
            gwas, triple, lit, gs
        MATCH
            (gwas)-[gl:GWAS_TO_LIT]-(lit)
    """
    _tail = """
        RETURN
            gwas {{.id, .trait}},
            gs {{.pval, .localCount}},
            triple {{.id, .subject_name, .object_name, .predicate}},
            lit {{.pubmed_id}}
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
        triple.id = "{semmed_triple_id}"
        """
        + _where
        + _tail
    )
    trait_triple = (
        _head
        + """
        gwas.trait {eq_symbol} "{trait}" AND
        triple.id = "{semmed_triple_id}"
        """
        + _where
        + _tail
    )

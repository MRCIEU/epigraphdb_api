class GwasEfo:
    _head = """
        MATCH
            (gwas:Gwas)-[r:GWAS_NLP_EFO]-(efo:Efo)
    """
    _where = """
        WHERE
            r.score > {score_threshold} AND
    """
    _tail = """
        RETURN
            gwas {{.id, .trait}},
            r {{.score}},
            efo {{.type, .value, .id}}
        ORDER BY
            r.score DESC
    """
    gwas_efo = (
        _head
        + _where
        + """
        gwas.trait {eq_symbol} "{trait}" AND
        efo.value {eq_symbol} "{efo_term}"
    """
        + _tail
    )
    gwas = (
        _head
        + _where
        + """
        gwas.trait {eq_symbol} "{trait}"
    """
        + _tail
    )
    efo = (
        _head
        + _where
        + """
            efo.value {eq_symbol} "{efo_term}"
    """
        + _tail
    )


class DiseaseEfo:
    _head = """
        MATCH
            (disease:Disease)-[r:MONDO_MAP_EFO]-(efo:Efo)
    """
    _where = """
        WHERE
    """
    _tail = """
        RETURN
            disease {{.id, .label}},
            efo {{.type, .value, .id}}
    """
    disease_efo = (
        _head
        + _where
        + """
        disease.label =~ "{disease_label}" AND
        efo.value {eq_symbol} "{efo_term}"
    """
        + _tail
    )
    disease = (
        _head
        + _where
        + """
        disease.label {eq_symbol} "{disease_label}"
    """
        + _tail
    )
    efo = (
        _head
        + _where
        + """
        efo.value {eq_symbol} "{efo_term}"
    """
        + _tail
    )


class GwasEfoDisease:
    _head = """
        MATCH
            (gwas:Gwas)-[ge:GWAS_NLP_EFO]-(efo:Efo)
            -[ed:MONDO_MAP_EFO]-(disease:Disease)
    """
    _where = """
        WHERE
            ge.score > {score_threshold} AND
    """
    _tail = """
        RETURN
            gwas {{.id, .trait}},
            ge {{.score}},
            efo {{.type, .value, .id}},
            disease {{.id, .label}}
    """
    gwas_efo_disease = (
        _head
        + _where
        + """
        gwas.trait {eq_symbol} "{trait}" AND
        efo.value {eq_symbol} "{efo_term}" AND
        disease.label {eq_symbol} "{disease_label}"
        """
        + _tail
    )
    gwas_disease = (
        _head
        + _where
        + """
        gwas.trait {eq_symbol} "{trait}" AND
        disease.label {eq_symbol} "{disease_label}"
        """
        + _tail
    )
    gwas_efo = (
        _head
        + _where
        + """
        gwas.trait {eq_symbol} "{trait}" AND
        efo.value {eq_symbol} "{efo_term}"
        """
        + _tail
    )
    efo_disease = (
        _head
        + _where
        + """
        efo.value {eq_symbol} "{efo_term}" AND
        disease.label {eq_symbol} "{disease_label}"
        """
        + _tail
    )
    gwas = (
        _head
        + _where
        + """
        gwas.trait {eq_symbol} "{trait}"
        """
        + _tail
    )
    efo = (
        _head
        + _where
        + """
        efo.value {eq_symbol} "{efo_term}"
        """
        + _tail
    )
    disease = (
        _head
        + _where
        + """
        disease.label {eq_symbol} "{disease_label}"
        """
        + _tail
    )

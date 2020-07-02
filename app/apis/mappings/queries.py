class GeneToProtein:
    _head = """
        MATCH
            (gene:Gene)-[gp:GENE_TO_PROTEIN]-(protein:Protein)
        WHERE
    """
    _tail = """
        RETURN
            gene {{.ensembl_id, .name}},
            protein {{.uniprot_id}}
    """
    by_name = (
        _head
        + """
            gene.name IN {gene_name_list}
    """
        + _tail
    )
    by_id = (
        _head
        + """
            gene.ensembl_id IN {gene_id_list}
    """
        + _tail
    )

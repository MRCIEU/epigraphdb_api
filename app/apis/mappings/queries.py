class GeneToProtein:
    query = """
        MATCH
            (gene:Gene)-[gp:GENE_TO_PROTEIN]-(protein:Protein)
        WHERE
            gene.name IN {gene_list}
        RETURN
            gene {{.ensembl_id, .name}},
            protein {{.uniprot_id}}
    """

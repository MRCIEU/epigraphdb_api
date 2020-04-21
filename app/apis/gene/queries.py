class Druggability:
    ppi = """
            MATCH
                (g1:Gene)-[:GENE_TO_PROTEIN]-(p1:Protein)
                -[:INTACT_INTERACTS_WITH | STRING_INTERACT_WITH]-
                (p2:Protein)-[:GENE_TO_PROTEIN]-(g2:Gene)
            WHERE
                g1.name = '{gene_name}' AND
                g2.name IS NOT NULL AND
                g2.druggability_tier IS NOT NULL
            RETURN DISTINCT
                g1 {{.name}},
                p1 {{.uniprot_id}},
                p2 {{.uniprot_id}},
                g2 {{.name, .druggability_tier}}
            ORDER BY
                g2.druggability_tier, g2.name
    """


class Literature:
    query = """
        MATCH
            (gene:Gene)-[:SEM_GENE]-(:SemmedTerm)-[:SEM_SUB|SEM_OBJ]-
            (st:SemmedTriple)-[:SEM_TO_LIT]-(l:Literature)
        WHERE
            gene.name = '{gene_name}' AND
            st.object_name=~"(?i).*{object_name}.*"
        RETURN
            gene {{.name}},
            st {{.predicate, .object_name}},
            collect(l.pubmed_id) AS pubmed_id
    """

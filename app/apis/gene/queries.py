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
            (gene:Gene)-[:TERM_TO_GENE]-(lt_gene:LiteratureTerm)-[st:SEMMEDDB_PREDICATE]->(lt:LiteratureTerm)
        WHERE
            gene.name = '{gene_name}' AND
            lt.name =~ "(?i).*{object_name}.*"
        WITH
            gene, lt_gene, st, lt
        MATCH
            (triple:LiteratureTriple)-[triple_to_lit:SEMMEDDB_TO_LIT]-(l:Literature)
        WHERE
            triple.subject_id = lt_gene.id AND
            triple.object_id = lt.id AND
            triple.predicate = st.predicate
        RETURN
            gene {{.name}},
            st {{.predicate}},
            lt {{.id, .name, .type}},
            collect(l.id) AS pubmed_id
    """


class Drugs:
    query = """
        MATCH
            (gene:Gene)-[r:OPENTARGETS_DRUG_TO_TARGET|CPIC]-(drug:Drug)
        WHERE
            gene.name = '{gene_name}'
        RETURN
            gene {{.name}},
            r,
            type(r) AS r_source,
            drug {{.label}}
    """

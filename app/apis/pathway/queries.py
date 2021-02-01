class PathwayQueries:
    pathway = """
    MATCH
        (gwas:Gwas {{trait: "{trait}"}})
        -[gwas_to_variant:GWAS_TO_VARIANT]->(variant:Variant)-[variant_to_gene:VARIANT_TO_GENE]->
        (gene:Gene)-[gene_to_protein:GENE_TO_PROTEIN]->(protein:Protein)
        -[protein_in_pathway:PROTEIN_IN_PATHWAY]->(pathway:Pathway)
    WHERE
        gwas_to_variant.pval < {pval_threshold} AND
        gene.name is not null
    RETURN
        gwas {{.id, .trait}},
        gwas_to_variant
            {{.beta, .se, .pval, .samplesize}},
        variant {{.name}},
        gene {{.name}},
        protein {{.uniprot_id}},
        pathway {{.id, .name}}
    ORDER BY gwas_to_variant.pval
    ;
    """

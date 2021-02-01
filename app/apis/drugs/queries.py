class DrugsQueries:
    risk_factors = """
    MATCH
        (trait:Gwas {{trait: "{trait}"}})<-[mr:MR_EVE_MR]-(assoc_trait:Gwas)
        -[gwas_to_variant:GWAS_TO_VARIANT]->(variant:Variant)
        -[:VARIANT_TO_GENE]->(gene:Gene)
        <-[:CPIC|:OPENTARGETS_DRUG_TO_TARGET]-(drug:Drug)
    WHERE
        trait.trait <> assoc_trait.trait AND
        mr.pval < {pval_threshold} AND
        gwas_to_variant.pval < 1e-8
    RETURN
        trait {{.id, .trait}},
        assoc_trait {{.id, .trait}},
        variant {{.name}},
        gene {{.name}},
        drug {{.label}},
        mr {{.b, .se, .pval, .selection, .method, .moescore}}
    ORDER BY mr.pval
    ;
    """.replace(
        "\n", " "
    )

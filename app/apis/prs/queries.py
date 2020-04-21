class PrsQueries:
    prs = """
    MATCH
        (trait:Gwas)-[prs:PRS]-(assoc_trait:Gwas)
    WHERE
        trait.trait = "{trait}" AND
        prs.p < {pval_threshold}
    RETURN
        trait {{.id, .trait}},
        assoc_trait {{.id, .trait}},
        prs {{
            .beta,
            .se,
            .p,
            .r2,
            .nsnps,
            .n,
            .model
        }}
    ORDER BY
        prs.p
    ;
    """.replace(
        "\n", " "
    )

class GeneticCorQueries:
    genetic_cor = """
    MATCH
        (trait:Gwas)-[gc:GEN_COR]-(assoc_trait:Gwas)
    WHERE
        trait.trait = "{trait}" AND
        abs(gc.rg) > {cor_coef_threshold}
    RETURN
        trait {{.id, .trait}},
        assoc_trait {{.id, .trait}},
        gc {{
          .Z, .p,
          .rg, .rg_SE,
          .rg_intercept, .rg_intercept_SE,
          .h2, .h2_SE,
          .h2_intercept, .h2_intercept_SE
        }}
    ORDER BY
        gc.rg DESC
    ;
    """.replace(
        "\n", " "
    )

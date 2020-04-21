class GeneticCorQueries:
    genetic_cor = """
    MATCH
        (trait:Gwas)-[gc:BN_GEN_COR]-(assoc_trait:Gwas)
    WHERE
        trait.trait = "{trait}" AND
        abs(gc.rg) > {cor_coef_threshold}
    RETURN
        trait {{.id, .trait}},
        assoc_trait {{.id, .trait}},
        gc {{
          .rg,
          .z, .se, .p,
          .h2_int, .h2_int_se,
          .h2_obs, .h2_obs_se,
          .gcov_int, .gcov_int_se
        }}
    ORDER BY
        gc.rg DESC
    ;
    """.replace(
        "\n", " "
    )

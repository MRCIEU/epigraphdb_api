class ObsCorQueries:
    gwas_obs_cor = """
    MATCH
        (trait:Gwas)-[obs_cor:OBS_COR]-(assoc_trait:Gwas)
    WHERE
        trait.trait = "{trait}" AND
        abs(obs_cor.cor) > {cor_coef_threshold}
    RETURN
        trait {{.id, .trait}},
        assoc_trait {{.id, .trait}},
        obs_cor {{.cor}}
    ORDER BY
        obs_cor.cor DESC
    ;
    """.replace(
        "\n", " "
    )

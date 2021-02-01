class Proteins:

    simple = """
    MATCH
        (e:Exposure)<-[n:SENS_EXP]-(s)-[m:SENS_OUT]->
        (o:Outcome)<-[r:MR]-(e:Exposure)<-[i:INST_EXP]-()
    WHERE
        e.expID = "{query}" AND r.pvalue < toFloat("{pvalue}")
        AND s.rs_ID = i.rs_ID
    RETURN DISTINCT
        s.expID AS expID, s.outID AS outID, s.outID_mrbase AS outID_mrbase,
        r.nsnp AS nsnp, r.pvalue AS pvalue, s.rs_ID AS rsID,
        s.direction AS direction,
        s.steiger_pvalue AS steiger_pvalue, s.coloc_prob AS coloc_prob,
        r.beta AS beta, r.method AS method, i.trans_cis AS trans_cis,
        toFloat(r.mr_hetero_pvalue) AS q_pvalue,
        s.ld_score AS ld_check,
        r.se AS se
    ORDER BY
        pvalue, outID;
    """.replace(
        "\n", " "
    )

    mrres = """
    MATCH
        (e:Exposure)<-[n:SENS_EXP]-(s)-[m:SENS_OUT]->
        (o:Outcome)<-[r:MR]-(e:Exposure)
    WHERE
        e.expID = "{query}" AND r.pvalue < toFloat("{pvalue}")
    RETURN DISTINCT
        r.expID AS expID, r.outID AS outID, r.outID_mrbase AS outID_mrbase,
        r.nsnp AS nsnp, r.method AS method,
        r.beta AS beta, r.se AS se, r.pvalue AS pvalue
    ORDER BY
        pvalue, outID;
    """.replace(
        "\n", " "
    )

    sglmr = """
    MATCH
        (e:Exposure)<-[n:SENS_EXP]-(s)-[m:SENS_OUT]->
        (o:Outcome)<-[r:MR]-(e:Exposure)<-[i:INST_EXP]-()
    WHERE
        e.expID = "{query}" AND r.pvalue < toFloat("{pvalue}")
        AND s.rs_ID = i.rs_ID
    RETURN DISTINCT
        s.rs_ID AS rsID, s.expID AS expID, s.outID AS outID,
        s.outID_mrbase AS outID_mrbase, s.tier AS tier,
        s.beta_sgl AS beta_sgl, s.se_sgl AS se_slg, s.pvalue_sgl AS pvalue_sgl,
        i.trans_cis AS trans_cis
    ORDER BY
        pvalue_sgl, outID;
    """.replace(
        "\n", " "
    )

    inst = """
    MATCH
        (e:Exposure)<-[n:INST_EXP]-(i)-[m:INST_OUT]->
        (o:Outcome)<-[r:MR]-(e:Exposure)
    WHERE
        e.expID = "{query}" AND r.pvalue < toFloat("{pvalue}")
    RETURN DISTINCT
        n.rs_ID AS rsID, n.expID AS expID, m.outID AS outID,
        m.outID_mrbase AS outID_mrbase,
        n.ea AS ea, n.nea AS nea, n.eaf_exp AS eaf_exp,
        n.samplesize_exp AS sample_exp, m.samplesize_out AS sample_out,
        n.author_exp AS author_exp, m.author_out AS author_out,
        n.trans_cis AS trans_cis, r.pvalue AS pvalue
    ORDER BY
        pvalue, outID;
    """

    sense = """
    MATCH
        (e:Exposure)<-[n:SENS_EXP]-(s)-[m:SENS_OUT]->
        (o:Outcome)<-[r:MR]-(e:Exposure)<-[i:INST_EXP]-()
    WHERE
        e.expID = "{query}"
        AND r.pvalue < toFloat("{pvalue}")
        AND s.rs_ID = i.rs_ID
    RETURN DISTINCT
        s.rs_ID AS rsID, s.expID AS expID, s.outID AS outID,
        s.outID_mrbase AS outID_mrbase, s.direction AS direction,
        s.steiger_pvalue AS steiger_pvalue, s.coloc_prob AS coloc_prob,
        i.trans_cis AS trans_cis,
        toFloat(r.mr_hetero_pvalue) AS q_pvalue,
        s.ld_score AS ld_check, s.outcome_snp AS outcome_snp,
        s.tier AS tier, r.pvalue AS pvalue
    ORDER BY
        pvalue, outID;
    """.replace(
        "\n", " "
    )


class NonProteins:

    simple = """
    MATCH
        (o:Outcome)<-[n:SENS_OUT]-(s)-[m:SENS_EXP]->(e:Exposure)-[r:MR]->
        (o:Outcome)<-[INST_OUT]-()-[i:INST_EXP]->()
    WHERE
        o.outID = "{query}" AND r.pvalue < toFloat("{pvalue}")
        AND s.rs_ID = i.rs_ID AND s.expID = i.expID
    RETURN DISTINCT
        s.expID AS expID, s.outID AS outID, s.outID_mrbase AS outID_mrbase,
        r.nsnp AS nsnp, r.pvalue AS pvalue, s.rs_ID AS rsID,
        s.direction AS direction, s.steiger_pvalue AS steiger_pvalue,
        s.coloc_prob AS coloc_prob, r.beta AS beta, r.method AS method,
        i.trans_cis AS trans_cis,
        toFloat(r.mr_hetero_pvalue) AS q_pvalue,
        s.ld_score AS ld_check, r.se AS se
    ORDER BY
        pvalue, expID;
    """.replace(
        "\n", " "
    )

    mrres = """
    MATCH
        (o:Outcome)<-[n:SENS_OUT]-(s)-[m:SENS_EXP]->
        (e:Exposure)-[r:MR]->(o:Outcome)
    where
        o.outID = "{query}" AND r.pvalue < toFloat("{pvalue}")
    RETURN DISTINCT
        r.expID AS expID, r.outID AS outID, r.outID_mrbase AS outID_mrbase,
        r.nsnp AS nsnp, r.method AS method,
        r.beta AS beta, r.se AS se, r.pvalue AS pvalue
    ORDER BY
        pvalue, expID;
    """.replace(
        "\n", " "
    )

    # NOTE: `se_slg` should have been `se_sgl`, but
    #       not fixing to keep compatibility with downstream
    sglmr = """
    MATCH (o:Outcome)<-[n:SENS_OUT]-(s)-[m:SENS_EXP]->(e:Exposure)-[r:MR]->
          (o:Outcome)<-[INST_OUT]-()-[i:INST_EXP]->()
    WHERE
        o.outID = "{query}" AND r.pvalue < toFloat("{pvalue}")
        AND s.rs_ID = i.rs_ID AND s.expID = i.expID
    RETURN DISTINCT
        s.rs_ID AS rsID, s.expID AS expID, s.outID AS outID,
        s.outID_mrbase AS outID_mrbase, s.tier AS tier,
        s.beta_sgl AS beta_sgl, s.se_sgl AS se_slg, s.pvalue_sgl AS pvalue_sgl,
        i.trans_cis AS trans_cis
    ORDER BY
        pvalue_sgl, expID;
    """.replace(
        "\n", " "
    )

    inst = """
    MATCH
        (o:Outcome)<-[m:INST_OUT]-(i)-[n:INST_EXP]->
        (e:Exposure)-[r:MR]->(o:Outcome)
    WHERE
        o.outID = "{query}" AND r.pvalue < toFloat("{pvalue}")
    RETURN DISTINCT
        n.rs_ID AS rsID, n.expID AS expID, m.outID AS outID,
        m.outID_mrbase AS outID_mrbase,
        n.ea AS ea, n.nea AS nea, n.eaf_exp AS eaf_exp,
        n.samplesize_exp AS sample_exp, m.samplesize_out AS sample_out,
        n.author_exp AS author_exp, m.author_out AS author_out,
        n.trans_cis AS trans_cis, r.pvalue AS pvalue
    ORDER BY
        pvalue, expID;
    """.replace(
        "\n", " "
    )

    sense = """
    MATCH
        (o:Outcome)<-[n:SENS_OUT]-(s)-[m:SENS_EXP]->
        (e:Exposure)-[r:MR]->(o:Outcome)<-[INST_OUT]-()-[i:INST_EXP]->()
    WHERE
        o.outID = "{query}" AND r.pvalue < toFloat("{pvalue}")
        AND s.rs_ID = i.rs_ID AND s.expID = i.expID
    RETURN DISTINCT
        s.rs_ID AS rsID, s.expID AS expID, s.outID AS outID,
        s.outID_mrbase AS outID_mrbase, s.direction AS direction,
        s.steiger_pvalue AS steiger_pvalue, s.coloc_prob AS coloc_prob,
        i.trans_cis AS trans_cis,
        toFloat(r.mr_hetero_pvalue) AS q_pvalue,
        s.ld_score AS ld_check,
        s.outcome_snp AS outcome_snp, s.tier AS tier, r.pvalue AS pvalue
    ORDER BY
        pvalue, expID;
    """.replace(
        "\n", " "
    )


class Pleio:

    count = """
    MATCH
    (i:Instruments)-[INST_EXP]->(e:Exposure)
    WHERE
        i.rs_ID="{rsid}"
    RETURN DISTINCT
        count(e.expID) AS pt_count;
    """.replace(
        "\n", " "
    )

    non_count = """
    MATCH
        (i:Instruments)-[INST_EXP]->(e:Exposure)
    WHERE
        i.rs_ID = "{rsid}"
    RETURN DISTINCT
        e.expID AS expID;
    """.replace(
        "\n", " "
    )

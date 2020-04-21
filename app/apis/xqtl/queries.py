class XqtlMultiSnpMr:
    _head = """
        MATCH (gene:Gene)-[r:XQTL_MULTI_SNP_MR]->(gwas:Gwas)
        """
    _tail = """
            AND
            gene.name is not null AND
            r.mr_method = "{mr_method}" AND
            r.qtl_type = "{qtl_type}" AND
            r.p < {pval_threshold}
        RETURN
            gene {{.ensembl_id, .name}},
            gwas {{.id, .trait}},
            r {{.beta, .se, .p}}
        ORDER BY
            r.p
        ;
        """
    exposure = (
        _head
        + """
        WHERE gene.name = "{exposure}"
        """
        + _tail
    ).replace("\n", " ")
    outcome = (
        _head
        + """
        WHERE gwas.trait = "{outcome}"
        """
        + _tail
    ).replace("\n", " ")
    exposure_outcome = (
        _head
        + """
        WHERE gene.name = "{exposure}"
        AND gwas.trait = "{outcome}"
        """
        + _tail
    ).replace("\n", " ")


class XqtlSingleSnpMr:
    _head = """
        MATCH
            (variant:Variant)-[s:XQTL_SINGLE_SNP_MR_SNP_GENE]->
            (gene:Gene)-[r:XQTL_SINGLE_SNP_MR_GENE_GWAS]->(gwas:Gwas)
        """
    _tail = """
            AND
            gene.name is not null AND
            variant.name = r.rsid AND
            r.qtl_type = "{qtl_type}" AND
            r.p < {pval_threshold}
        RETURN
            gene {{.ensembl_id, .name}},
            gwas {{.id, .trait}},
            r {{.beta, .se, .p, .rsid}}
        ORDER BY
            r.p
        ;
        """
    exposure = (
        _head
        + """
        WHERE gene.name = "{exposure}"
        """
        + _tail
    ).replace("\n", " ")

    outcome = (
        _head
        + """
        WHERE gwas.trait = "{outcome}"
        """
        + _tail
    ).replace("\n", " ")

    variant = (
        _head
        + """
        WHERE variant.name = "{variant}"
        """
        + _tail
    ).replace("\n", " ")

    exposure_outcome = (
        _head
        + """
        WHERE gene.name = "{exposure}"
        AND gwas.trait = "{outcome}"
        """
        + _tail
    ).replace("\n", " ")

    exposure_snp = (
        _head
        + """
        WHERE gene.name = "{exposure}"
        AND variant.name = "{variant}"
        """
        + _tail
    ).replace("\n", " ")

    outcome_snp = (
        _head
        + """
        WHERE gwas.trait = "{outcome}"
        AND variant.name = "{variant}"
        """
        + _tail
    ).replace("\n", " ")

    exposure_outcome_snp = (
        _head
        + """
        WHERE gene.name = "{exposure}"
        AND gwas.trait = "{outcome}"
        AND variant.name = "{variant}"
        """
        + _tail
    ).replace("\n", " ")


class GeneByVariant:
    query = """
        MATCH
            (variant:Variant)-[vg:XQTL_SINGLE_SNP_MR_SNP_GENE]-(gene:Gene)
            -[xqtl:XQTL_SINGLE_SNP_MR_GENE_GWAS]-(gwas:Gwas)
        WHERE
            variant.name IN {variant_list} AND
            xqtl.rsid = variant.name AND
            xqtl.qtl_type = '{qtl_type}'
        WITH variant.name AS variant, collect(DISTINCT gene.name) AS gene_list
        RETURN
            variant, gene_list, size(gene_list) AS n_genes
        """


class XqtlSingleSnpMrList:
    gene_gwas = """
        MATCH
            (gene:Gene)-[r:XQTL_SINGLE_SNP_MR_GENE_GWAS]->(gwas:Gwas)
        WHERE
            r.qtl_type = "{qtl_type}" AND
            r.p < {pval_threshold}
        RETURN
            gene {{.name}},
            gwas {{.id, .trait}}
        ;
    """
    gwas = """
        MATCH
            (gene:Gene)-[r:XQTL_SINGLE_SNP_MR_GENE_GWAS]->(gwas:Gwas)
        WHERE
            r.qtl_type = "{qtl_type}" AND
            r.p < {pval_threshold}
        RETURN
            gwas {{.id, .trait}}
        ;
    """
    gene = """
        MATCH
            (gene:Gene)-[r:XQTL_SINGLE_SNP_MR_GENE_GWAS]->(gwas:Gwas)
        WHERE
            r.qtl_type = "{qtl_type}" AND
            r.p < {pval_threshold}
        RETURN
            gene {{.ensembl_id, .name}}
        ;
    """

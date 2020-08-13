from pathlib import Path

import pandas as pd
from starlette.testclient import TestClient

from app.main import app
from app.utils import df_coerce

client = TestClient(app)

CASE_1_DIR = Path("data/case-study-results/case-1")
GWAS_TRAIT = "Coronary heart disease"
QTL_TYPE = "eQTL"
SNP = "rs11065979"
PPI_N_INTERMEDIATE_PROTEINS = 1


def get_sys_snps(gwas_trait, qtl_type):
    # Get snps associated with the trait
    route = "/xqtl/single-snp-mr"
    params = {
        "outcome_trait": gwas_trait,
        "qtl_type": qtl_type,
        "pval_threshold": 1e-08,
    }
    r = client.get(route, params=params)
    r.raise_for_status()
    snps = pd.json_normalize(r.json()["results"])["r.rsid"].drop_duplicates()
    # Get genes associated by the snp
    route = "/xqtl/single-snp-mr/gene-by-variant"
    payload = {"qtl_type": qtl_type, "variant_list": snps.to_list()}
    r = client.post(route, json=payload)
    r.raise_for_status()
    res = pd.json_normalize(r.json()["results"])["variant"].rename("snp")
    return res


def get_snp_protein(snp, qtl_type):
    # get snp-gene
    route = "/xqtl/single-snp-mr"
    params = {
        "variant": snp,
        "qtl_type": qtl_type,
        # NOTE: we don't restrict pvalue
        "pval_threshold": 1.0,
    }
    r = client.get(route, params=params)
    r.raise_for_status()
    snp_gene_df = pd.json_normalize(r.json()["results"])[
        ["r.rsid", "gene.name"]
    ].drop_duplicates()
    # get gene-protein
    route = "/mappings/gene-to-protein"
    payload = {"gene_name_list": snp_gene_df["gene.name"].to_list()}
    r = client.post(route, json=payload)
    r.raise_for_status()
    protein_df = pd.json_normalize(r.json()["results"])
    if len(protein_df) > 0:
        res_df = snp_gene_df.rename(
            columns={"r.rsid": "snp", "gene.name": "protein_name"}
        ).merge(
            protein_df[["gene.name", "protein.uniprot_id"]].rename(
                columns={
                    "gene.name": "protein_name",
                    "protein.uniprot_id": "uniprot_id",
                }
            ),
            left_on="protein_name",
            right_on="protein_name",
        )
    else:
        return pd.DataFrame(columns=["snp", "protein_name", "uniprot_id"])
    return res_df


def get_sys_proteins(sys_snps: pd.Series, qtl_type):
    res_df = (
        sys_snps.to_frame()
        .assign(
            protein_list=lambda df: df["snp"].apply(
                lambda x: get_snp_protein(snp=x, qtl_type=qtl_type)[
                    "uniprot_id"
                ].to_list()
            )
        )
        .assign(
            n_proteins=lambda df: df["protein_list"].apply(lambda x: len(x))
        )
    )
    return res_df


def get_protein_pathway(snp_protein_df):
    route = "/protein/in-pathway"
    payload = {"uniprot_id_list": snp_protein_df["uniprot_id"].to_list()}
    r = client.post(route, json=payload)
    r.raise_for_status()
    df = pd.json_normalize(r.json()["results"])

    if len(df) > 0:
        res_df = snp_protein_df[["uniprot_id"]].merge(
            df, left_on="uniprot_id", right_on="uniprot_id", how="left"
        )
    else:
        res_df = (
            snp_protein_df[["uniprot_id"]]
            .assign(pathway_count=None)
            .assign(pathway_reactome_id=None)
        )
    res_df = res_df.assign(
        pathway_count=lambda df: df["pathway_count"]
        .apply(lambda x: 0 if pd.isna(x) else x)
        .astype(int)
    ).assign(
        pathway_reactome_id=lambda df: df["pathway_reactome_id"].apply(
            lambda x: [] if not isinstance(x, list) else x
        )
    )
    return res_df


def get_ppi(snp_protein_df, n_intermediate_proteins: int = 0):
    route = "/protein/ppi/pairwise"
    payload = {
        "uniprot_id_list": snp_protein_df["uniprot_id"].to_list(),
        "n_intermediate_proteins": n_intermediate_proteins,
    }
    r = client.post(route, json=payload)
    r.raise_for_status()
    df = pd.json_normalize(r.json()["results"])

    if len(df) > 0:
        res_df = (
            snp_protein_df[["uniprot_id"]]
            .rename(columns={"uniprot_id": "protein"})
            .merge(df, left_on="protein", right_on="protein", how="left")
        )
    else:
        res_df = (
            snp_protein_df[["uniprot_id"]]
            .rename(columns={"uniprot_id": "protein"})
            .assign(assoc_protein=None, path_size=None)
        )
    return res_df


def test_snps_and_proteins():
    # snps
    snps = get_sys_snps(gwas_trait=GWAS_TRAIT, qtl_type=QTL_TYPE)
    snps_expected = pd.read_json(CASE_1_DIR / "case-1-snps.json", typ="series")
    assert (
        snps.sort_values().reset_index(drop=True).tolist()
        == snps_expected.sort_values().reset_index(drop=True).tolist()
    )
    # proteins
    proteins_df = get_sys_proteins(sys_snps=snps, qtl_type=QTL_TYPE)
    proteins_df_expected = pd.read_json(CASE_1_DIR / "case-1-proteins.json")
    pd.testing.assert_frame_equal(
        proteins_df.pipe(df_coerce, list_columns=["protein_list"]),
        proteins_df_expected.pipe(df_coerce, list_columns=["protein_list"]),
    )


def test_pathway():
    proteins_df = get_snp_protein(snp=SNP, qtl_type=QTL_TYPE)
    pathway_df = get_protein_pathway(proteins_df)
    pathway_df_expected = pd.read_json(CASE_1_DIR / "case-1-pathway-df.json")
    pd.testing.assert_frame_equal(
        pathway_df.pipe(df_coerce, list_columns=["pathway_reactome_id"]),
        pathway_df_expected.pipe(
            df_coerce, list_columns=["pathway_reactome_id"]
        ),
    )


def test_ppi():
    proteins_df = get_snp_protein(snp=SNP, qtl_type=QTL_TYPE)
    ppi_df = get_ppi(
        proteins_df, n_intermediate_proteins=PPI_N_INTERMEDIATE_PROTEINS
    )
    ppi_df_expected = pd.read_json(CASE_1_DIR / "case-1-ppi-df.json")
    pd.testing.assert_frame_equal(
        ppi_df.pipe(df_coerce), ppi_df_expected.pipe(df_coerce)
    )

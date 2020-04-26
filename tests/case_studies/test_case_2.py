import json
from pathlib import Path

import pandas as pd
from starlette.testclient import TestClient

from app.main import app
from app.utils import df_coerce

client = TestClient(app)

CASE_2_DIR = Path("data/case-study-results/case-2")
GENE_NAME = "IL23R"
OUTCOME_TRAIT = "Inflammatory bowel disease"


def ppi():
    route = "/gene/druggability/ppi"
    params = {"gene_name": GENE_NAME}
    r = client.get(url=route, params=params)
    r.raise_for_status()
    df = pd.json_normalize(r.json()["results"])
    return df


def extract_mr(outcome_trait, gene_list, qtl_type):
    route = "/xqtl/single-snp-mr"

    def per_gene(gene_name):
        params = {
            "exposure_gene": gene_name,
            "outcome_trait": outcome_trait,
            "qtl_type": qtl_type,
            "pval_threshold": 1e-5,
        }
        r = client.get(route, params=params)
        try:
            r.raise_for_status()
            df = pd.json_normalize(r.json()["results"])
            return df
        except:
            return None

    res_df = pd.concat(
        [per_gene(gene_name=gene_name) for gene_name in gene_list]
    ).reset_index(drop=True)
    return res_df


def extract_literature(outcome_trait, gene_list):
    def per_gene(gene_name):
        route = "/gene/literature"
        params = {"gene_name": gene_name, "object_name": outcome_trait.lower()}
        r = client.get(url=route, params=params)
        try:
            r.raise_for_status()
            res_df = pd.json_normalize(r.json()["results"])
            if len(res_df) > 0:
                res_df = res_df.assign(
                    literature_count=lambda df: df["pubmed_id"].apply(
                        lambda x: len(x)
                    )
                )
                return res_df
        except:
            return None

    res_df = pd.concat(
        [per_gene(gene_name=gene_name) for gene_name in gene_list]
    ).reset_index(drop=True)
    return res_df


def test_ppi():
    ppi_df = ppi()
    ppi_df_expected = pd.read_json(CASE_2_DIR / "case-2-ppi.json")
    pd.testing.assert_frame_equal(
        ppi_df.pipe(df_coerce), ppi_df_expected.pipe(df_coerce)
    )


def test_mr():
    gene_list_file = CASE_2_DIR / "case-2-gene-list.json"
    with gene_list_file.open() as f:
        gene_list = json.load(f)

    mr_df = pd.concat(
        [
            extract_mr(
                outcome_trait=OUTCOME_TRAIT,
                gene_list=gene_list,
                qtl_type=qtl_type,
            ).assign(qtl_type=qtl_type)
            for qtl_type in ["pQTL", "eQTL"]
        ]
    ).reset_index(drop=True)
    mr_df_expected = pd.read_json(CASE_2_DIR / "case-2-mr.json")
    pd.testing.assert_frame_equal(
        mr_df.pipe(df_coerce), mr_df_expected.pipe(df_coerce)
    )


def test_literature():
    gene_list_file = CASE_2_DIR / "case-2-gene-list.json"
    with gene_list_file.open() as f:
        gene_list = json.load(f)
    literature_df = extract_literature(
        outcome_trait=OUTCOME_TRAIT, gene_list=gene_list
    )
    literature_df_expected = pd.read_json(
        CASE_2_DIR / "case-2-literature.json"
    )

    pd.testing.assert_frame_equal(
        literature_df.pipe(df_coerce, list_columns=["pubmed_id"]),
        literature_df_expected.pipe(df_coerce, list_columns=["pubmed_id"]),
    )

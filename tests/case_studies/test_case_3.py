from pathlib import Path

import pandas as pd
from starlette.testclient import TestClient

from app.main import app
from app.utils import df_coerce

client = TestClient(app)

CASE_3_DIR = Path("data/case-study-results/case-3")
STARTING_TRAIT = "Sleep duration"
GWAS_ID = "ieu-a-1088"
ASSOC_GWAS_ID = "ieu-a-6"


def get_mr(trait):
    route = "/mr"
    params = {
        "exposure_trait": trait,
        "pval_threshold": 1e-10,
    }
    r = client.get(route, params=params)
    r.raise_for_status()
    mr_df = pd.json_normalize(r.json()["results"])
    return mr_df


def trait_to_disease(row):
    route = "/ontology/gwas-efo-disease"
    params = {
        "trait": row["outcome.trait"],
    }
    r = client.get(route, params=params)
    r.raise_for_status()
    disease_df = pd.json_normalize(r.json()["results"])
    if "disease.label" in disease_df:
        return disease_df["disease.label"].drop_duplicates()


def get_literature(gwas_id, assoc_gwas_id):
    route = "/literature/gwas/pairwise"
    params = {
        "gwas_id": gwas_id,
        "assoc_gwas_id": assoc_gwas_id,
        "by_gwas_id": "true",
        "pval_threshold": 1e-1,
        "semmantic_types": ["nusq", "dsyn"],
        "blacklist": "True",
        "limit": 1000,
    }
    r = client.get(route, params=params)
    r.raise_for_status()
    lit_df = pd.json_normalize(r.json()["results"])
    lit_df = lit_df.sort_values(by=["gs1.pval"], ascending=True)
    return lit_df


def test_mr():
    mr_df = get_mr(trait=STARTING_TRAIT)
    mr_df_expected = pd.read_json(CASE_3_DIR / "case-3-mr.json")
    pd.testing.assert_frame_equal(
        mr_df.pipe(df_coerce), mr_df_expected.pipe(df_coerce)
    )


def test_disease():
    disease_df = get_mr(trait=STARTING_TRAIT).assign(
        disease=lambda df: df.apply(trait_to_disease, axis=1)
    )
    disease_df_expected = pd.read_json(CASE_3_DIR / "case-3-disease.json")
    pd.testing.assert_frame_equal(
        disease_df.pipe(
            df_coerce,
            order_by=["exposure.id", "outcome.id", "mr.method"],
            list_columns=["disease"],
        ),
        disease_df_expected.pipe(
            df_coerce,
            order_by=["exposure.id", "outcome.id", "mr.method"],
            list_columns=["disease"],
        ),
    )


def test_literature():
    lit_df = get_literature(gwas_id=GWAS_ID, assoc_gwas_id=ASSOC_GWAS_ID)
    lit_df_expected = pd.read_json(CASE_3_DIR / "case-3-lit.json")
    pd.testing.assert_frame_equal(
        lit_df.pipe(
            df_coerce,
            order_by=[
                "s1.subject_name",
                "s1.predicate",
                "s1.object_name",
                "s2.subject_name",
                "s2.predicate",
                "s2.object_name",
            ],
        ),
        lit_df_expected.pipe(
            df_coerce,
            order_by=[
                "s1.subject_name",
                "s1.predicate",
                "s1.object_name",
                "s2.subject_name",
                "s2.predicate",
                "s2.object_name",
            ],
        ),
    )

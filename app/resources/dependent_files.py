from pathlib import Path

DATA_DIR = Path(__file__).parent.parent.parent / "data"

dependent_files = {
    "gene_id_exclude": (DATA_DIR / "gene-id-exclude.txt"),
    "covid-xqtl": (DATA_DIR / "covid-xqtl.sqlite"),
    "xqtl_pwas_mr": (DATA_DIR / "xqtl_pwas_mr.db"),
    "sc-eqtl-mr": (DATA_DIR / "sc-eqtl-mr.db"),
}

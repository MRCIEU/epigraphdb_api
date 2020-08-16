from pathlib import Path

DATA_DIR = Path(__file__).parent.parent.parent / "data"

dependent_files = {
    "gene_id_exclude": (DATA_DIR / "gene-id-exclude.txt"),
    "covid-xqtl": (DATA_DIR / "covid-xqtl.sqlite"),
}

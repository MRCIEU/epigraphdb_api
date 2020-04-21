from pathlib import Path

DATA_DIR = Path(__file__).parent.parent.parent / "data"

dependent_files = {
    "gene_id_exclude": (DATA_DIR / "gene-id-exclude.txt"),
    "covid-xqtl": (DATA_DIR / "covid-xqtl.sqlite"),
}

for name, path in dependent_files.items():
    # TODO: implement logging level
    # logger.info(f"Dependent file {name}: {path}")
    if not path.exists():
        raise OSError(2, "No such file or directory", str(path))

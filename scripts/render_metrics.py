from pprint import pformat
from typing import Any, Dict

import pandas as pd
from jinja2 import Environment, FileSystemLoader
from loguru import logger
from starlette.testclient import TestClient
from typing_extensions import TypedDict

from app.main import app

from .doc_utils import OUTPUT_DIR, TEMPLATE_DIR

TEMPLATE_NAME = "metrics.md"
OUTPUT_PATH = OUTPUT_DIR / "metrics.md"


class MetricsData(TypedDict):
    meta_node_count_table: str
    meta_rel_count_table: str
    metadata_info: str


def make_meta_node_count_table(raw_results: Dict[str, Any]) -> str:
    node_df = (
        pd.DataFrame.from_dict(raw_results["nodes"], orient="index")
        .reset_index()
        .rename(columns={"index": "Meta node"})[["Meta node", "count"]]
        .assign(count=lambda df: df["count"].apply(lambda x: f"{x:,}"))
        .sort_values(by=["Meta node"])
        .set_index("Meta node")
    )
    logger.info("node_df: {node_df.head()}")
    res = node_df.to_markdown()
    return res


def make_meta_rel_count_table(raw_results: Dict[str, Any]) -> str:
    rel_df = (
        pd.json_normalize(raw_results["connections"])
        .rename(columns={"rel": "Meta rel"})
        .assign(count=lambda df: df["count"].apply(lambda x: f"{x:,}"))
        .sort_values(by=["from_node", "to_node", "count"])
        .set_index("Meta rel")
    )
    logger.info("rel_df: {rel_df.head()}")
    res = rel_df.to_markdown()
    return res


def make_metadata_info(raw_results: Dict[str, Any]) -> str:
    # Add 4 spaces indentation to each line
    formatted_lines = [
        "    " + line for line in pformat(raw_results).split("\n")
    ]
    res = "\n".join(formatted_lines)
    return res


def main():
    # init
    client = TestClient(app)
    template_loader = FileSystemLoader(TEMPLATE_DIR)
    env = Environment(loader=template_loader)
    template = env.get_template(TEMPLATE_NAME)
    r = client.get("/meta/schema", params={"graphviz": False, "plot": False})
    r.raise_for_status()
    response_results = r.json()
    # processing
    logger.info("meta_node_count_table")
    meta_node_count_table = make_meta_node_count_table(response_results)
    logger.info("meta_rel_count_table")
    meta_rel_count_table = make_meta_rel_count_table(response_results)
    logger.info("metadata_info")
    metadata_info = make_metadata_info(response_results)
    # render
    metrics_data: MetricsData = {
        "meta_node_count_table": meta_node_count_table,
        "meta_rel_count_table": meta_rel_count_table,
        "metadata_info": metadata_info,
    }
    rendered_doc = template.render(**metrics_data)
    logger.info(f"write to {OUTPUT_PATH}")
    with OUTPUT_PATH.open("w") as f:
        f.write(rendered_doc)


if __name__ == "__main__":
    main()

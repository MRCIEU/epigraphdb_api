from pprint import pformat
from typing import List

from jinja2 import Environment, FileSystemLoader
from loguru import logger
from starlette.testclient import TestClient
from typing_extensions import TypedDict

from app.main import app
from epigraphdb_common_utils.epigraphdb_schema import (
    DataDictNode,
    DataDictRel,
    meta_nodes_dict,
    meta_rels_dict,
)

from .doc_utils import (
    OUTPUT_DIR,
    TEMPLATE_DIR,
    MetaEntityProp,
    entity_sneak_peek,
)

TEMPLATE_NAME_NODE = "meta-nodes.md"
TEMPLATE_NAME_REL = "meta-relationships.md"
OUTPUT_PATH_NODE = OUTPUT_DIR / "meta-nodes.md"
OUTPUT_PATH_REL = OUTPUT_DIR / "meta-relationships.md"


class MetaNodeData(TypedDict):
    name: str
    desc: str
    id_prop: str
    name_prop: str
    props: List[MetaEntityProp]
    sneak_peek_query: str
    sneak_peek_result: str


class MetaRelData(TypedDict):
    name: str
    desc: str
    path: str
    props: List[MetaEntityProp]
    sneak_peek_query: str
    sneak_peek_result: str


def prep_meta_node_data(
    name: str, value: DataDictNode, client: TestClient
) -> MetaNodeData:
    desc = "\n".join([f"> {_}" for _ in value.doc.split("\n")])
    props: List[MetaEntityProp] = []
    if len(value.properties) > 0:
        props = [
            {
                "name": name,
                "type": value.type,
                "required": value.required,
                "desc": "\n".join(
                    [f"  {_}" for _ in value.doc.split("\n")]
                ).strip(),
            }
            for name, value in value.properties.items()
        ]
    sneak_peek_query, sneak_peek_result = entity_sneak_peek(
        meta_entity=name, entity_type="node", client=client
    )
    formatted_query = f"    {sneak_peek_query}"
    formatted_result = "\n".join(
        [f"    {line}" for line in pformat(sneak_peek_result).split("\n")]
    )
    res: MetaNodeData = {
        "name": name,
        "desc": desc,
        "id_prop": value.id,
        "name_prop": value.name,
        "props": props,
        "sneak_peek_query": formatted_query,
        "sneak_peek_result": formatted_result,
    }
    return res


def prep_meta_rel_data(
    name: str, value: DataDictRel, client: TestClient
) -> MetaRelData:
    desc = "\n".join([f"> {_}" for _ in value.doc.split("\n")])
    path = "({source})-[{rel}]->({target})".format(
        source=value.source, target=value.target, rel=name
    )
    props: List[MetaEntityProp] = []
    if len(value.properties) > 0:
        props = [
            {
                "name": name,
                "type": value.type,
                "required": value.required,
                "desc": "\n".join(
                    [f"  {_}" for _ in value.doc.split("\n")]
                ).strip(),
            }
            for name, value in value.properties.items()
        ]
    sneak_peek_query, sneak_peek_result = entity_sneak_peek(
        meta_entity=name, entity_type="rel", client=client
    )
    formatted_query = f"    {sneak_peek_query}"
    formatted_result = "\n".join(
        [f"    {line}" for line in pformat(sneak_peek_result).split("\n")]
    )
    res: MetaRelData = {
        "name": name,
        "desc": desc,
        "path": path,
        "props": props,
        "sneak_peek_query": formatted_query,
        "sneak_peek_result": formatted_result,
    }
    return res


def main():
    # init
    client = TestClient(app)
    template_loader = FileSystemLoader(TEMPLATE_DIR)
    env = Environment(loader=template_loader)
    # meta node
    logger.info("Process meta nodes")
    meta_node_template = env.get_template(TEMPLATE_NAME_NODE)
    meta_nodes_list: List[MetaNodeData] = [
        prep_meta_node_data(name, value, client=client)
        for name, value in meta_nodes_dict.items()
    ]
    meta_node_template_data = {"meta_nodes_list": meta_nodes_list}
    rendered_doc_node = meta_node_template.render(**meta_node_template_data)
    logger.info(f"write to {OUTPUT_PATH_NODE}")
    with OUTPUT_PATH_NODE.open("w") as f:
        f.write(rendered_doc_node)
    # meta rel
    logger.info("Process meta rels")
    meta_rel_template = env.get_template(TEMPLATE_NAME_REL)
    meta_rels_list: List[MetaRelData] = [
        prep_meta_rel_data(name, value, client=client)
        for name, value in meta_rels_dict.items()
    ]
    meta_rel_template_data = {"meta_rels_list": meta_rels_list}
    rendered_doc_rel = meta_rel_template.render(**meta_rel_template_data)
    logger.info(f"write to {OUTPUT_PATH_REL}")
    with OUTPUT_PATH_REL.open("w") as f:
        f.write(rendered_doc_rel)


if __name__ == "__main__":
    main()

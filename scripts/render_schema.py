from pprint import pformat

from epigraphdb_common_utils.epigraphdb_data_dicts import (
    meta_nodes_dict_sanitised,
    meta_rels_dict_sanitised,
)

from .render_api import render_results_get


def rmd_render_meta_nodes(api_url: str):
    for name, data in meta_nodes_dict_sanitised.items():
        print(f"## `{name}`\n")

        if data["doc"] is not None:
            print("> ", data["doc"], "\n")

        if data["id"] is not None:
            print("**`id` property**: `{id}`\n".format(id=data["id"],))
        if data["name"] is not None:
            print(
                "**`label` property**: `{label}`\n".format(label=data["name"],)
            )

        if data["properties"] is not None:
            print("**Properties**:\n")
            render_properties(data["properties"])
            print("\n")

        # if name not in INVALID_NODES:
        render_entity_sneak_peek(name, "node", api_url)


def rmd_render_meta_rels(api_url: str):
    for name, data in meta_rels_dict_sanitised.items():
        print(f"## `{name}`\n")

        if data["doc"] is not None:
            print("> ", data["doc"], "\n")

        print(
            "**Path**: `({source})-[{name}]->({target})`\n".format(
                source=data["source"], target=data["target"], name=name
            )
        )

        if data["properties"] is not None:
            print("**Properties**:\n")
            render_properties(data["properties"])
            print("\n")

        render_entity_sneak_peek(name, "rel", api_url)


def render_properties(property):
    for key, value in property.items():
        if value is None:
            print("- `{prop}`\n".format(prop=key))
        else:
            print("- `{prop}`: {doc}\n".format(prop=key, doc=value))


def render_entity_sneak_peek(meta_entity: str, entity_type: str, api_url: str):

    sneak_peek_res = sneak_peek(meta_entity, entity_type, api_url)

    print('???+ summary \\"**Examples**\\"\n')
    print("    **query**\n")
    print("    ```")
    print("    ", sneak_peek_res["query"])
    print("    ```")
    print("\n")
    print("    **data**\n")
    print("    ```json")
    for line in pformat(sneak_peek_res["results"]).split("\n"):
        print("    ", line)
    print("    ```")
    print("\n")


def sneak_peek(meta_entity: str, entity_type: str, api_url: str):
    params = {"limit": 3, "offset": 0}
    if entity_type == "node":
        route = f"/meta/nodes/{meta_entity}/list"
    elif entity_type == "rel":
        route = f"/meta/rels/{meta_entity}/list"
    url = f"{api_url}{route}"
    results = render_results_get(url=url, params=params)
    res = {
        "query": results["metadata"]["query"],
        "results": results["results"],
    }
    return res

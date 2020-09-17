from epigraphdb_common_utils.epigraphdb_data_dicts import (
    meta_nodes_dict_sanitised,
    meta_rels_dict_sanitised,
)


def rmd_render_meta_nodes():
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


def rmd_render_meta_rels():
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


def render_properties(property):
    for key, value in property.items():
        if value is None:
            print("- `{prop}`\n".format(prop=key))
        else:
            print("- `{prop}`: {doc}\n".format(prop=key, doc=value))

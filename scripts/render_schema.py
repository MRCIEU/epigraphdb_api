from pprint import pprint

from app.models.schema_meta_nodes import meta_node_schema
from app.models.schema_meta_rels import meta_path_schema, meta_rel_schema


def format_schema(orig_schema):
    # keys = orig_schema.keys()
    # schema = {
    #     "properties": {
    #         key: {"type": value["type"]}
    #         for key, value in orig_schema["properties"].items()
    #     },
    #     "required": orig_schema["required"] if "required" in keys else {},
    # }
    schema = orig_schema
    return schema


def rmd_render_meta_nodes():
    for name, model in meta_node_schema.items():
        schema = format_schema(model.schema())
        print(f"## `{name}`\n")

        if "description" in list(model.schema().keys()):
            print("**Description**:\n")
            print(model.schema()["description"], "\n")

        print("**Schema**:\n")
        print("```")
        pprint(schema)
        print("```")


def rmd_render_meta_rels():
    for name, model in meta_rel_schema.items():
        schema = format_schema(model.schema())
        path = meta_path_schema[name]
        print(f"## `{name}`\n")

        if "description" in list(model.schema().keys()):
            print("**Description**:\n")
            print(model.schema()["description"], "\n")

        print(f"**Path**: `({path[0]})-[{name}]->({path[1]})`\n")

        print("**Schema**:\n")
        print("```")
        pprint(schema)
        print("```")

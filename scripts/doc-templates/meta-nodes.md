# EpiGraphDB meta nodes

This document shows the current meta nodes (a group of node entities) in
the EpiGraphDB graph database. For each meta node, their available
properties are shown, and an example set of node entities are shown in
the collapsed text box.

{% for meta_node in meta_nodes_list %}

## `{{ meta_node["name"] }}`

{{ meta_node["desc"] }}

**`_id` property**: `{{ meta_node["id_prop"] }}`

**`_name` property**: `{{ meta_node["name_prop"] }}`

{% if meta_node["props"]|length > 0  %}
**Properties**:

  {% for prop in meta_node["props"] %}
- `{{ prop["name"] }}`: `{{ prop["type"] }}`{% if prop["required"] %}, **required**{% else %}, *optional*{% endif %}; {{ prop["desc"] }}
  {% endfor %}
{% endif  %}

???+ summary "**Examples**"

    **query**

    ```
{{ meta_node["sneak_peek_query"] }}
    ```

    **data**

    ```json
{{ meta_node["sneak_peek_result"] }}
    ```

{% endfor %}

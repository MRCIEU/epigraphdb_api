# EpiGraphDB meta relationships

This document shows the current meta relationships (a group of relationship entities) in the EpiGraphDB graph database.
For each meta relationship, their available properties are shown, and an example set of relationship entities are shown in the collapsed text box.

{% for meta_rel in meta_rels_list %}

## `{{ meta_rel["name"] }}`

{{ meta_rel["desc"] }}

**Path**: `{{ meta_rel["path"] }}`

{% if meta_rel["props"]|length > 0  %}
**Properties**:

  {% for prop in meta_rel["props"] %}
- `{{ prop["name"] }}`: `{{ prop["type"] }}`; {{ prop["desc"] }}
  {% endfor %}
{% endif  %}

???+ summary "**Examples**"

    **query**

    ```
{{ meta_rel["sneak_peek_query"] }}
    ```

    **data**

    ```json
{{ meta_rel["sneak_peek_result"] }}
    ```

{% endfor %}

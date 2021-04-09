## `{{ name }}`

{% if desc is not none %}
> ```
{{ desc }}
> ```
{% endif %}

**Params**

``` {python}
{{ params }}
```

{% for example in examples %}
??? summary "**{{ example.title }}**"

    **Script**

    ```{python}
{{ example["script"]  }}
    ```

    **Results**

    ```{json}
{{ example["result"]  }}
    ```

{% endfor %}

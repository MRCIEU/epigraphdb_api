from pprint import pformat
from textwrap import dedent
from typing import Optional

import requests


def render_query(route: str, params, method: str = "GET") -> str:
    get_query = """
    import requests


    url = f'{{EPIGRAPHDB_API_URL}}{route}'
    params = {params}
    r = requests.get(url, params=params)
    r.raise_for_status()
    r.json()
    """.format(
        route=route, params=str(params)
    )
    post_query = """
    import requests


    url = f'{{EPIGRAPHDB_API_URL}}{route}'
    data = {params}
    r = requests.post(url, json=data)
    r.raise_for_status()
    r.json()
    """.format(
        route=route, params=str(params)
    )
    query = get_query
    if method == "POST":
        query = post_query
    query = dedent(query)
    return query


def render_results_get(url: str, params):
    r = requests.get(url=url, params=params)
    r.raise_for_status()
    return r.json()


def render_results_post(url: str, params):
    r = requests.post(url=url, json=params)
    r.raise_for_status()
    return r.json()


def render_results(
    api_url: str,
    route: str,
    params,
    char_limit: Optional[int] = 2400,
    method: str = "GET",
) -> str:
    url = f"{api_url}{route}"
    func = render_results_get
    if method == "POST":
        func = render_results_post
    results = func(url=url, params=params)
    res = pformat(results)
    if char_limit is not None:
        return res[:char_limit]
    else:
        return res


def rmd_render_endpoints(api_url, endpoint_params):
    for endpoint, config in endpoint_params.items():

        print(f"## `{endpoint}`\n")

        if config["func"].__doc__ is not None:
            desc = dedent(config["func"].__doc__).strip()
        else:
            desc = ""
        for line in desc.split("\n"):
            print(">      ", line)
        print("\n")

        print("**Params**\n")
        print("````{python}")
        print(pformat(config["func"].__annotations__))
        print("````")

        for i, test in enumerate(config["tests"]):
            if "endpoint" in test.keys():
                actual_endpoint = test["endpoint"]
            else:
                actual_endpoint = endpoint
            method, route = actual_endpoint.split(" ")

            if "desc" in test.keys():
                desc = test["desc"]
            else:
                desc = "Query"
            params = test["params"]

            query = render_query(route=route, params=params, method=method)
            results = render_results(
                api_url=api_url, route=route, params=params, method=method
            )

            print("\n")
            print(f'??? summary \\"**{i + 1}. {desc}**\\"\n')
            print("    **Script**\n")
            print("    ```{python}")
            for line in query.split("\n"):
                print("    ", line)
            print("    ```")
            print("\n")
            print("    **Results**\n")
            print("    ```{json}")
            for line in results.split("\n"):
                print("    ", line)
            print("    ```")
            print("\n")

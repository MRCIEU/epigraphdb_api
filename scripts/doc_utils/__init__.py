from pathlib import Path
from pprint import pformat
from textwrap import dedent
from typing import Any, Dict, Optional, Tuple

from starlette.testclient import TestClient
from typing_extensions import TypedDict

TEMPLATE_DIR = Path("scripts") / "doc-templates"
OUTPUT_DIR = Path("output")


class MetaEntityProp(TypedDict):
    name: str
    type: str
    desc: str
    required: bool


def entity_sneak_peek(
    meta_entity: str, entity_type: str, client: TestClient
) -> Tuple[str, str]:
    params = {"limit": 3, "offset": 0}
    if entity_type == "node":
        url = f"/meta/nodes/{meta_entity}/list"
    elif entity_type == "rel":
        url = f"/meta/rels/{meta_entity}/list"
    results = render_results_get(url=url, params=params, client=client)
    res = (
        results["metadata"]["query"],
        results["results"],
    )
    return res


def render_query(route: str, params, method: str = "GET") -> str:
    get_query = """
    import requests


    url = 'https://api.epigraphdb.org{route}'
    params = {params}
    r = requests.get(url, params=params)
    r.raise_for_status()
    r.json()
    """.format(
        route=route, params=str(params)
    )
    post_query = """
    import requests


    url = 'https://api.epigraphdb.org{route}'
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


def render_results_get(url: str, params, client: TestClient):
    r = client.get(url=url, params=params)
    r.raise_for_status()
    return r.json()


def render_results_post(url: str, params, client: TestClient):
    r = client.post(url=url, json=params)
    r.raise_for_status()
    return r.json()


def render_results(
    url: str,
    params: Optional[Dict[str, Any]],
    client: TestClient,
    char_limit: Optional[int] = 2400,
    method: str = "GET",
) -> str:
    func = render_results_get
    if method == "POST":
        func = render_results_post
    results = func(url=url, params=params, client=client)
    res = pformat(results)
    if char_limit is not None:
        return res[:char_limit]
    else:
        return res

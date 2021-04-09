from pprint import pformat
from textwrap import dedent
from typing import Callable, List, Optional

import jinja2
from jinja2 import Environment, FileSystemLoader
from loguru import logger
from starlette.testclient import TestClient
from typing_extensions import TypedDict

from app.main import app
from app.resources import public_endpoints

from .doc_utils import OUTPUT_DIR, TEMPLATE_DIR, render_query, render_results

TEMPLATE_NAME_MAIN = "api-endpoints.md"
TEMPLATE_NAME_ENDPOINT = "api-endpoints-endpoint.md"
OUTPUT_PATH = OUTPUT_DIR / "api-endpoints.md"


class EndpointExample(TypedDict):
    title: str
    script: str
    result: str


class ApiEndpointData(TypedDict):
    name: str
    desc: Optional[str]
    params: str
    examples: List[EndpointExample]


class EndpointRenderedText(TypedDict):
    rendered_text: str


class RenderedTemplateData(TypedDict):
    topic_endpoints: List[EndpointRenderedText]
    utility_endpoints: List[EndpointRenderedText]


def process_data(
    endpoint_name: str,
    endpoint_data: public_endpoints.EndpointData,
    client: TestClient,
) -> ApiEndpointData:
    logger.info(f"Process endpoint {endpoint_name}")
    func = endpoint_data["func"]
    endpoint_desc: Optional[str] = None
    if func.__doc__ is not None:
        endpoint_desc = "\n".join(
            [f">   {_}" for _ in dedent(func.__doc__).split("\n")]
        )
    endpoint_params = pformat(func.__annotations__)
    endpoint_examples: List[EndpointExample] = [
        process_example(
            _,
            idx=idx + 1,
            func=func,
            endpoint_name=endpoint_name,
            client=client,
        )
        for idx, _ in enumerate(endpoint_data["tests"])
    ]
    res: ApiEndpointData = {
        "name": endpoint_name,
        "desc": endpoint_desc,
        "params": endpoint_params,
        "examples": endpoint_examples,
    }
    return res


def process_example(
    example_data: public_endpoints.EndpointExample,
    idx: int,
    func: Callable,
    endpoint_name: str,
    client: TestClient,
) -> EndpointExample:
    if "endpoint" in example_data.keys():
        endpoint = example_data["endpoint"]
    else:
        endpoint = endpoint_name
    method, url = endpoint.split(" ")
    params = example_data["params"]
    title = "Query"
    if "desc" in example_data.keys():
        title = example_data["desc"]
    title = f"{idx}. {title}"
    script = render_query(route=url, params=params, method=method)
    result = render_results(
        url=url, params=params, client=client, method=method
    )
    script_formatted = "\n".join([f"    {_}" for _ in script.split("\n")])
    result_formatted = "\n".join([f"    {_}" for _ in result.split("\n")])
    res: EndpointExample = {
        "title": title,
        "script": script_formatted,
        "result": result_formatted,
    }
    return res


def render_text(
    data: ApiEndpointData, endpoint_template: jinja2.environment.Template
) -> EndpointRenderedText:
    rendered_text = endpoint_template.render(**data)
    res: EndpointRenderedText = {"rendered_text": rendered_text}
    return res


def main():
    # init
    client = TestClient(app)
    template_loader = FileSystemLoader(TEMPLATE_DIR)
    env = Environment(loader=template_loader)
    main_template = env.get_template(TEMPLATE_NAME_MAIN)
    endpoint_template = env.get_template(TEMPLATE_NAME_ENDPOINT)
    # processing
    topic_endpoints_data: List[ApiEndpointData] = [
        process_data(key, value, client=client)
        for key, value in public_endpoints.topic_params.items()
    ]
    utility_endpoints_data: List[ApiEndpointData] = [
        process_data(key, value, client=client)
        for key, value in public_endpoints.util_params.items()
    ]
    topic_endpoints_rendered_text: List[EndpointRenderedText] = [
        render_text(_, endpoint_template) for _ in topic_endpoints_data
    ]
    utility_endpoints_rendered_text: List[EndpointRenderedText] = [
        render_text(_, endpoint_template) for _ in utility_endpoints_data
    ]
    rendered_template_data: RenderedTemplateData = {
        "topic_endpoints": topic_endpoints_rendered_text,
        "utility_endpoints": utility_endpoints_rendered_text,
    }
    rendered_doc = main_template.render(**rendered_template_data)
    # output
    logger.info(f"write to {OUTPUT_PATH}")
    with OUTPUT_PATH.open("w") as f:
        f.write(rendered_doc)


if __name__ == "__main__":
    main()

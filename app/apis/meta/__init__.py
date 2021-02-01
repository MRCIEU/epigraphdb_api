import json
from typing import Dict, List, Optional

import yaml
from fastapi import APIRouter, HTTPException, Query
from pydantic.schema import model_schema
from starlette.responses import FileResponse

from app.models import ApiGenericResponse
from app.models.api_meta_graph import (
    EpigraphdbMetaNodes,
    EpigraphdbMetaNodesFull,
    EpigraphdbMetaRels,
)
from app.models.schema_meta_nodes import (
    meta_node_id_name_mappings,
    meta_node_schema,
)
from app.models.schema_meta_rels import meta_path_schema, meta_rel_schema
from app.settings import api_private_access, epigraphdb
from app.utils.logging import log_args, logger
from app.utils.schema import (
    generate_schema,
    render_graphviz,
    render_schema_graphviz,
)
from app.utils.validators import validate_at_least_one_not_none

from .functions import (
    nodes_neighbour_query_builder,
    nodes_search_query_builder,
    paths_search_query_builder,
)
from .queries import MetaQueries

router = APIRouter()


@router.get("/meta/schema")
def get_schema(
    graphviz: bool = False, plot: bool = False, overwrite: bool = False
):
    """Schema of EpiGraphDB Graph.
    """
    log_args(api="/meta/schema")
    schema = generate_schema(overwrite=overwrite)
    if graphviz and not plot:
        dot = render_schema_graphviz(schema)
        res = dot.source
    elif graphviz and plot:
        dot = render_schema_graphviz(schema)
        schema_file = render_graphviz(dot, overwrite=overwrite)
        return FileResponse(schema_file, media_type="image/png")
    else:
        res = schema
    return res


@router.get("/meta/nodes/list", response_model=List[str])
def meta_nodes_list():
    """List meta nodes
    """
    log_args(api="/meta/nodes/list")
    res = [_.value for _ in EpigraphdbMetaNodes]
    return res


@router.get(
    "/meta/nodes/id-name-schema", response_model=Dict[str, Dict[str, str]]
)
def meta_nodes_id_name_schema():
    """Show the current id / name schema for meta nodes."""
    log_args(api="/meta/nodes/id-name-schema")
    res = meta_node_id_name_mappings
    return res


@router.get("/meta/nodes/{meta_node}/list", response_model=ApiGenericResponse)
def nodes_list(
    meta_node: EpigraphdbMetaNodesFull,
    full_data: bool = True,
    limit: int = Query(10, ge=1, le=10_000),
    offset: int = 0,
):
    """List nodes under a meta node.

    - `limit`: If you supply full_data to be True, the limit is 500,
      otherwise the limit is 10,000
    - `full_data`: When False, only return the id and name fields for
      a node.
      For the specific id and name fields, refer to /meta/nodes/id-name-schema.
    """
    log_args(api="/meta/nodes/{meta_node}/list", kwargs=locals())
    if full_data:
        full_data_limit = 500
        if limit > full_data_limit:
            raise HTTPException(
                status_code=422,
                detail=f"limit should be less equal than {full_data_limit}.",
            )
        query = MetaQueries.get_nodes.format(
            meta_node=meta_node.value, skip=offset, limit=limit
        )
    else:
        id_field = meta_node_id_name_mappings[meta_node.value]["id"]
        name_field = meta_node_id_name_mappings[meta_node.value]["name"]
        query = MetaQueries.get_node_id_and_name_fields.format(
            meta_node=meta_node.value,
            id_field=id_field,
            name_field=name_field,
            limit=limit,
            offset=offset,
        )
    logger.info(query)
    response = epigraphdb.run_query(query)
    return response


@router.get(
    "/meta/nodes/{meta_node}/search", response_model=ApiGenericResponse
)
def nodes_search(
    meta_node: str,
    id: Optional[str] = None,
    name: Optional[str] = None,
    limit: int = Query(10, ge=1, le=200),
    full_data: bool = True,
):
    """Use `id` for exact match, and use `name` for fuzzy match.

    - full_data: If False, only returns basic info (id, name).
    """
    log_args(api="/meta/nodes/{meta_node}/search", kwargs=locals())
    validate_at_least_one_not_none(dict(id=id, name=name))
    query = nodes_search_query_builder(
        meta_node=meta_node, id=id, name=name, limit=limit, full_data=full_data
    )
    logger.info(query)
    response = epigraphdb.run_query(query)
    return response


@router.get(
    "/meta/nodes/{meta_node}/search-neighbour",
    response_model=ApiGenericResponse,
)
def nodes_search_neighbour(
    meta_node: str, id: Optional[str], limit: int = Query(50, ge=1, le=200)
):
    """Search the neighbour nodes adjacent to the query node.
    """
    log_args(api="/meta/nodes/{meta_node}/search-neighbour", kwargs=locals())
    query = nodes_neighbour_query_builder(
        meta_node=meta_node, id=id, limit=limit
    )
    logger.info(query)
    response = epigraphdb.run_query(query)
    return response


@router.get("/meta/rels/list", response_model=List[str])
def meta_rels_list():
    """List meta rels.
    """
    log_args(api="/meta/rels/list")
    res = [_.value for _ in EpigraphdbMetaRels]
    return res


@router.get("/meta/rels/{meta_rel}/list", response_model=ApiGenericResponse)
def rels_list(
    meta_rel: EpigraphdbMetaRels,
    limit: int = Query(10, ge=1, le=2000),
    offset: int = 0,
):
    """List relationships under a meta relationship.
    """
    log_args(api="/meta/rels/{meta_rel}/list", kwargs=locals())
    query = MetaQueries.get_rels.format(
        meta_rel=meta_rel.value, skip=offset, limit=limit
    )
    logger.info(query)
    response = epigraphdb.run_query(query)
    return response


@router.get("/meta/paths/search", response_model=ApiGenericResponse)
def get_paths_search(
    meta_node_source: str,
    id_source: str,
    meta_node_target: str,
    id_target: str,
    max_path_length: int = Query(3, ge=1, le=5),
    limit: int = Query(100, ge=1, le=500),
):
    log_args(api="/meta/paths/search", kwargs=locals())
    query = paths_search_query_builder(
        meta_node_source=meta_node_source,
        id_source=id_source,
        meta_node_target=meta_node_target,
        id_target=id_target,
        max_path_length=max_path_length,
        limit=limit,
    )
    logger.info(query)
    response = epigraphdb.run_query(query)
    return response


if api_private_access:

    @router.get("/meta/api/schema")
    def get_meta_api_schema(yaml_format: bool = False):
        """Returns current EpiGraphDB API schema, by default as json
        """
        res = {
            "meta_nodes": {
                meta_node: model_schema(model)  # type: ignore
                for meta_node, model in meta_node_schema.items()
            },
            "meta_rels": {
                meta_rel: model_schema(model)  # type: ignore
                for meta_rel, model in meta_rel_schema.items()
            },
            "meta_paths": {
                meta_rel: {"source": value[0], "target": value[1]}
                for meta_rel, value in meta_path_schema.items()
            },
        }
        if yaml_format:
            res = yaml.dump(yaml.load(json.dumps(res), Loader=yaml.FullLoader))
        return res

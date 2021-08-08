from datetime import datetime
from typing import Any, Dict, List

import requests
from fastapi import APIRouter, Query

from app.settings import neural_url

from . import models

router = APIRouter()


@router.get("/nlp/query/text", response_model=models.NlpQueryTextResponse)
def get_nlp_query_text(
    text: str,
    asis: bool = False,
    include_meta_nodes: List[str] = Query([]),
    limit: int = Query(50, ge=1, le=200),
):
    """Return EpiGraphDB entities that matches the input text
    via text embeddings.

    - `asis`: If False, apply builtin preprocessing to `text`
    - `include_meta_nodes`: Leave as is to search in all meta entities,
      otherwise limit to the supplied list
    """
    route = "/query/text"
    params: Dict[str, Any] = {
        "text": text,
        "asis": asis,
        "include_meta_nodes": include_meta_nodes,
        "limit": limit,
    }
    start_time = datetime.now()
    r = requests.get(f"{neural_url}{route}", params=params)
    try:
        r.raise_for_status()
        query_results = r.json()
        empty_results = False
    except:
        query_results = []
        empty_results = True
    finish_time = datetime.now()
    total_seconds = (finish_time - start_time).total_seconds()
    metadata = {"total_seconds": total_seconds, "empty_results": empty_results}
    res = {
        "metadata": metadata,
        "results": query_results,
    }
    return res


@router.get("/nlp/query/entity", response_model=models.NlpQueryEntityResponse)
def get_nlp_query_ent(
    entity_id: str,
    meta_node: str,
    include_meta_nodes: List[str] = Query([]),
    limit: int = Query(50, ge=1, le=200),
):
    """Return EpiGraphDB entities that matches the query entity
    via text embeddings.
    """
    route = "/query/entity"
    params: Dict[str, Any] = {
        "entity_id": entity_id,
        "meta_node": meta_node,
        "include_meta_nodes": include_meta_nodes,
        "limit": limit,
    }
    start_time = datetime.now()
    r = requests.get(f"{neural_url}{route}", params=params)
    try:
        r.raise_for_status()
        query_results = r.json()["results"]
        empty_results = False
    except:
        query_results = []
        empty_results = True
    finish_time = datetime.now()
    total_seconds = (finish_time - start_time).total_seconds()
    metadata = {"total_seconds": total_seconds, "empty_results": empty_results}
    res = {
        "metadata": metadata,
        "results": query_results,
    }
    return res


@router.get(
    "/nlp/query/entity/encode",
    response_model=models.NlpQueryEntityEncodeResponse,
)
def get_nlp_query_ent_encode(entity_id: str, meta_node: str):
    """Return the text embeddings of the queried entity"""
    route = "/query/entity/encode"
    params: Dict[str, Any] = {"entity_id": entity_id, "meta_node": meta_node}
    start_time = datetime.now()
    r = requests.get(f"{neural_url}{route}", params=params)
    try:
        r.raise_for_status()
        query_results = r.json()
        empty_results = False
    except:
        query_results = []
        empty_results = True
    finish_time = datetime.now()
    total_seconds = (finish_time - start_time).total_seconds()
    metadata = {"total_seconds": total_seconds, "empty_results": empty_results}
    res = {
        "metadata": metadata,
        "results": query_results,
    }
    return res

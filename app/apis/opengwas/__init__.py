from typing import Any, Dict, List

import requests
from fastapi import APIRouter
from pydantic import create_model_from_typeddict
from typing_extensions import TypedDict

from app.settings import neural_url
from app.utils.logging import log_args

router = APIRouter()


class GwasItem(TypedDict):
    id: str
    trait: str


class GwasRecommenderRes(TypedDict):
    empty: bool
    results: List[GwasItem]


GwasRecommenderResponse = create_model_from_typeddict(
    GwasRecommenderRes  # type: ignore
)


@router.get("/opengwas/search/id", response_model=GwasRecommenderResponse)
def get_gwas_recommender(gwas_id: str, limit: int = 30) -> GwasRecommenderRes:
    """GWAS recommender for the IEU OpenGWAS Database.

    For the input gwas_id returns a list of OpenGWAS studies
    curated in EpiGraphDB.
    """

    def _format(item: Dict[str, Any]) -> GwasItem:
        res: GwasItem = {
            "id": item["id"],
            "trait": item["name"],
        }
        return res

    log_args(api="/opengwas/search/id", kwargs=locals())
    # logics:
    # first try query using embeddings,
    # if it fails, try query using simple text matching
    embeddings_results = _search_by_embeddings(gwas_id=gwas_id, limit=limit)
    if len(embeddings_results) > 0:
        results = embeddings_results
        empty = False
    else:
        text_results = _search_by_text(gwas_id=gwas_id, limit=limit)
        empty = True if len(text_results) == 0 else False
        results = text_results
    res: GwasRecommenderRes = {
        "empty": empty,
        "results": [_format(_) for _ in results],
    }
    return res


def _search_by_embeddings(gwas_id: str, limit: int) -> List[Dict]:
    url = f"{neural_url}/query/entity"
    params: Dict[str, Any] = {
        "entity_id": gwas_id,
        "meta_node": "Gwas",
        "include_meta_nodes": ["Gwas"],
        "method": "embeddings",
        "limit": limit,
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    res = r.json()["results"]
    return res


def _search_by_text(gwas_id: str, limit: int) -> List[Dict]:
    url = f"{neural_url}/query/entity"
    params: Dict[str, Any] = {
        "entity_id": gwas_id,
        "meta_node": "Gwas",
        "include_meta_nodes": ["Gwas"],
        "method": "simple",
        "limit": limit,
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    res = r.json()["results"]
    return res

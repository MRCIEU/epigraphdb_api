from typing import Any, Dict

import requests
from fastapi import APIRouter

from app.models import ApiInfoBuilds
from app.resources.info import builds
from app.settings import epigraphdb, neural_url, pqtl, public_graph

router = APIRouter()


@router.get("/ping", response_model=bool)
def get_top_ping(dependencies: bool = True) -> bool:
    """Test that you are connected to the API."""
    if not dependencies:
        return True
    else:
        epigraphdb_ok = epigraphdb.check_connection()
        pqtl_ok = pqtl.check_connection()
        public_graph_ok = public_graph.check_connection()
        neural_ok = requests.get(f"{neural_url}/ping").ok
        all = [epigraphdb_ok, pqtl_ok, public_graph_ok, neural_ok]
        all_ok = sum(all) == len(all)
        return all_ok


@router.get("/builds", response_model=ApiInfoBuilds)
def get_top_builds() -> Dict[str, Any]:
    return builds

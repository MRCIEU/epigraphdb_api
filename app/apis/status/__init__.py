from typing import List

from fastapi import APIRouter, HTTPException

from app import settings
from app.models import EpigraphdbGraphs
from app.resources._global import get_service_builds
from app.settings import epigraphdb, pqtl
from app.utils.logging import log_args
from app.utils.ping import ping_service

from .models import GraphDbMetrics, PingResponse
from .queries import DbStatusQueries

router = APIRouter()
pqtl_disabled_metrics = ["schema", "graph_metadata"]


@router.get("/status/ping", response_model=List[PingResponse])
def get_ping():
    """Ping services and return their status.
    Return True if they are running else False.
    """
    data = [
        {
            "name": "epigraphdb_bolt",
            "url": f"bolt://{epigraphdb.hostname}/{epigraphdb.bolt_port}",
            "available": epigraphdb.check_connection(),
        },
        {
            "name": "pqtl_bolt",
            "url": f"bolt://{pqtl.hostname}/{pqtl.bolt_port}",
            "available": pqtl.check_connection(),
        },
        {
            "name": "epigraphdb_browser",
            "url": settings.epigraphdb_browser,
            "available": ping_service(settings.epigraphdb_browser),
        },
    ]
    log_args(api="status/ping")
    return data


@router.get("/status/api")
def get_api_metric():
    """Return API metrics:
    """
    log_args(api="/status/api")
    data = get_service_builds()
    return data


@router.get("/status/db")
def get_db_metric(
    metric: GraphDbMetrics, db: EpigraphdbGraphs = EpigraphdbGraphs.epigraphdb
):
    """Return database metrics.
    """
    log_args(api="/status/db", kwargs=locals())
    # NOTE: not every available metric is listed in the metrics model
    #       some needs special nodes, some needs APOC
    #       need to find a way to reconcile the two.
    if db.value == "epigraphdb":
        neo4j_db = epigraphdb
    elif db.value == "pqtl":
        neo4j_db = pqtl
        if metric.value in pqtl_disabled_metrics:
            raise HTTPException(
                status_code=422, detail="metric is not applicable for pqtl."
            )
    query = getattr(DbStatusQueries, metric.value)
    res = neo4j_db.run_query(query, format=False)
    return res

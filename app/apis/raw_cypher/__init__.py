"""
Pass cypher queries to neo4j databases.

When the API server is set up as a public server,
this endpoint requires a dedicated api_key to use.

When set up as a private server, the api_key is optional.
"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.api_key import APIKey

from app.models import EpigraphdbGraphsExtended
from app.settings import epigraphdb, pqtl  # noqa
from app.utils.api_key import get_api_key
from app.utils.database import Neo4jDB
from app.utils.logging import log_args, logger

from .models import RawCypherResponse

router = APIRouter()
summary = "Run cypher queries, reserved for internal use."


@router.get("/raw_cypher/", response_model=RawCypherResponse)
def get_raw_cyper(
    query: str,
    db: EpigraphdbGraphsExtended = EpigraphdbGraphsExtended.epigraphdb,
    hostname: Optional[str] = None,
    bolt_port: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    api_key: APIKey = Depends(get_api_key),
):
    """Query neo4j database using cypher command.

    "query": A qualified cypher query
    "db": epigraphdb (default), or pqtl
    """
    log_args(api="/raw_cypher", kwargs=locals())
    if db.value == "epigraphdb":
        logger.info("Query epigraphdb graph")
        neo4j_db = epigraphdb
    elif db.value == "pqtl":
        logger.info("Query pqtl graph")
        neo4j_db = pqtl
    elif db.value == "custom":
        if (
            hostname is not None
            and bolt_port is not None
            and user is not None
            and password is not None
        ):
            logger.info("Query custom graphs")
            neo4j_db = Neo4jDB(
                hostname=hostname,
                bolt_port=bolt_port,
                user=user,
                password=password,
            )
            if not neo4j_db.check_connection():
                raise HTTPException(
                    status_code=422, detail="Cannot connect to supplied graph"
                )
    res = cypher(query=query, neo4j_db=neo4j_db)
    return res


def cypher(query: str, neo4j_db: Neo4jDB):
    logger.info(query)
    data = neo4j_db.run_query(query)
    return data

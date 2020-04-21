from fastapi import APIRouter

from app.models import ApiGenericResponse
from app.settings import epigraphdb
from app.utils.database import Neo4jDB
from app.utils.logging import log_args

from . import models, queries

PUBLIC_GRAPH_HOSTNAME = "crashdown.epi.bris.ac.uk"
PUBLIC_GRAPH_PORT = "10086"

router = APIRouter()
public_graph = Neo4jDB(
    hostname=PUBLIC_GRAPH_HOSTNAME, bolt_port=PUBLIC_GRAPH_PORT
)


@router.post("/cypher", response_model=ApiGenericResponse)
def post_cypher(data: models.CypherRequest):
    """Send a cypher query to EpiGraphDB Graph.
    """
    res = public_graph.run_query(data.query)
    return res


@router.post(
    "/cypher/builder/plain",
    summary="""
Build and execute a cypher query.
""",
)
def post_cypher_builder_plain(data: models.CypherBuilderRequest):
    """
    Execute a plain cypher query of the following form:

    ```
    MATCH
        (source_node:{source_meta_node})
        -[rel:{meta_rel}]-
        (target_node:{target_meta_node})
    {
        WHERE [where0] AND [where1] AND ...
    }
    RETURN p
    {
       ORDER BY [order_by0], [order_by1], ...
    }
    LIMIT {limit}
    ```

    NOTE:
    - Please check API documentation for usage examples.
    - where: A list of strings where each is a cypher WHERE clause.
    - order_by: A list of strings where each is a cypher ORDER BY clase.
    It is only valid if your request contains valid where clauses
    - limit: Currently we limit maximum paths to 1000 (default to 100)
    """
    log_args(api="/cypher/builder/plain", kwargs=locals())
    where = ""
    order_by = ""
    if len(data.where) > 0:
        where = "WHERE " + "AND ".join(data.where)
    if data.order_by:
        order_by = "ORDER BY " + ", ".join(data.order_by)
    query = queries.CypherBuilder.query.format(
        source_meta_node=data.source_meta_node,
        meta_rel=data.meta_rel,
        target_meta_node=data.target_meta_node,
        where=where,
        order_by=order_by,
        limit=data.limit,
    )
    log_args(query=query)
    res = epigraphdb.run_query(query)
    return res

from fastapi import APIRouter

from app.models import ApiGenericResponse
from app.utils.database import Neo4jDB

from . import models

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

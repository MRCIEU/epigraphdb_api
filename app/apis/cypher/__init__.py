from fastapi import APIRouter

from app.models import ApiGenericResponse
from app.settings import public_graph

from . import models

router = APIRouter()


@router.post("/cypher", response_model=ApiGenericResponse)
def post_cypher(data: models.CypherRequest):
    """Send a cypher query to EpiGraphDB Graph."""
    res = public_graph.run_query(data.query)
    return res

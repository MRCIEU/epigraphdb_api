from fastapi import APIRouter

from app.settings import epigraphdb
from app.utils.logging import log_args

from . import models, queries

router = APIRouter()


@router.post("/protein/ppi")
def post_protein_ppi(data: models.PpiRequest):
    """
    For the list of proteins, returns their **directly**
    associated proteins in protein-protein-interactions
    """
    log_args(api="/protein/ppi", kwargs=locals())
    query = queries.Ppi.query.format(protein_list=str(data.uniprot_id_list))
    res = epigraphdb.run_query(query)
    return res


@router.post("/protein/ppi/pairwise")
def post_protein_ppi_graph(data: models.PpiGraphRequest):
    """
    For the list of proteins, returns a graph edgelist
    where they are connected via protein-protein-interactions,
    with configurable middle steps
    """
    log_args(api="/protein/ppi/pairwise", kwargs=locals())
    query = queries.Ppi.graph.format(
        protein_list=str(data.uniprot_id_list),
        n=(data.n_intermediate_proteins + 1),
    )
    res = epigraphdb.run_query(query)
    return res


@router.post("/protein/in-pathway")
def post_protein_pathway(data: models.PathwayRequest):
    """
    For the list of proteins, returns their associated
    pathway data
    """
    log_args(api="/protein/in-pathway", kwargs=locals())
    query = queries.Pathway.query.format(
        protein_list=str(data.uniprot_id_list)
    )
    res = epigraphdb.run_query(query)
    return res

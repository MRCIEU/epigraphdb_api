from fastapi import APIRouter

from app.settings import epigraphdb
from app.utils.logging import log_args

from . import models, queries

router = APIRouter()


@router.get(
    "/gene/druggability/ppi", response_model=models.GeneDrugPpiResponse
)
def get_gene_druggability_ppi(gene_name: str):
    """
    For a gene, search for its associated druggable genes
    via protein-protein-interaction (INTACT and STRING)
    """
    log_args(api="/gene/druggability/ppi", kwargs=locals())
    query = queries.Druggability.ppi.format(gene_name=gene_name)
    res = epigraphdb.run_query(query)
    return res


@router.get("/gene/literature", response_model=models.GeneLiteratureResponse)
def get_gene_literature(gene_name: str, object_name: str):
    """
    For a gene, search for its literature evidence
    related to a SemMedDB term
    """
    log_args(api="/gene/literature", kwargs=locals())
    query = queries.Literature.query.format(
        gene_name=gene_name, object_name=object_name
    )
    res = epigraphdb.run_query(query)
    return res


@router.get("/gene/drugs", response_model=models.GeneDrugsResponse)
def get_gene_drugs(gene_name: str):
    """
    Get the aasociated drugs for a gene.
    """
    log_args(api="/gene/drugs", kwargs=locals())
    query = queries.Drugs.query.format(gene_name=gene_name)
    res = epigraphdb.run_query(query)
    return res

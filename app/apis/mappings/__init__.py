from fastapi import APIRouter

from app.settings import epigraphdb
from app.utils.logging import log_args

from . import models, queries

router = APIRouter()


@router.post("/mappings/gene-to-protein")
def post_gene_to_protein(data: models.GeneToProteinRequest):
    """
    Return protein uniprot_id from associated gene names
    """
    log_args(api="/mappings/gene-to-protein", kwargs=locals())
    query = queries.GeneToProtein.query.format(
        gene_list=str(data.gene_name_list)
    )
    res = epigraphdb.run_query(query)
    return res

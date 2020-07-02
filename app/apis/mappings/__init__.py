from fastapi import APIRouter

from app.settings import epigraphdb
from app.utils.logging import log_args
from app.utils.validators import validate_at_least_one_not_none

from . import models, queries

router = APIRouter()


@router.post("/mappings/gene-to-protein")
def post_gene_to_protein(data: models.GeneToProteinRequest):
    """
    Return protein uniprot_id from associated genes.

    - `gene_name_list`: List of HGNC symbols of the genes (default).
    - `gene_id_list`: List of Ensembl gene IDs (when `by_gene_id == True`)
    """
    log_args(api="/mappings/gene-to-protein", kwargs=locals())
    if data.by_gene_id:
        validate_at_least_one_not_none(dict(gene_id_list=data.gene_id_list))
        query = queries.GeneToProtein.by_id.format(
            gene_id_list=str(data.gene_id_list)
        )
    else:
        validate_at_least_one_not_none(
            dict(gene_name_list=data.gene_name_list)
        )
        query = queries.GeneToProtein.by_name.format(
            gene_name_list=str(data.gene_name_list)
        )
    res = epigraphdb.run_query(query)
    return res

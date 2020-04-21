from typing import List, Optional

from fastapi import APIRouter, Query

from app.settings import epigraphdb
from app.utils import cypher_fuzzify
from app.utils.logging import log_args
from app.utils.validators import (
    validate_at_least_one_not_none,
    validate_char_length,
)

from . import queries

router = APIRouter()


@router.get("/literature/gwas")
def get_literature_gwas_semmed(
    trait: Optional[str] = None,
    gwas_id: Optional[str] = None,
    semmed_triple_id: Optional[str] = None,
    semmed_predicates: List[str] = Query([]),
    by_gwas_id: bool = False,
    pval_threshold: float = Query(1e-3, ge=0, le=1e-1),
    limit: int = Query(50, ge=1, le=1000),
    skip: int = 0,
    fuzzy: bool = True,
):
    """
    Search for literature evidence of a Gwas trait via semmed.

    - `semmed_triple_id`: search for a specific semmed triple id,
      e.g. "ghrelin:INHIBITS:Leptin"
    - `semmed_predicates`: list of predicates for **whitelist**
    - `by_gwas_id`: False. If True search by Gwas.id
    - `fuzzy`: True. By default fuzzy match trait name.
    - `skip`: pagination
    """
    log_args(api="/literature/gwas", kwargs=locals())
    semmed_predicates_clause = ""
    if len(semmed_predicates) > 0:
        semmed_predicates_clause = "AND triple.predicate IN [{clause}]".format(
            clause=",".join(
                [f"'{predicate}'" for predicate in semmed_predicates]
            )
        )
    if by_gwas_id:
        validate_at_least_one_not_none(dict(gwas_id=gwas_id))
        if semmed_triple_id is not None:
            query = queries.Gwas.id_triple.format(
                gwas_id=gwas_id,
                semmed_triple_id=semmed_triple_id,
                semmed_predicates_clause=semmed_predicates_clause,
                pval_threshold=pval_threshold,
                skip=skip,
                limit=limit,
            )
        else:
            query = queries.Gwas.id.format(
                gwas_id=gwas_id,
                semmed_predicates_clause=semmed_predicates_clause,
                pval_threshold=pval_threshold,
                limit=limit,
                skip=skip,
            )
    else:
        validate_at_least_one_not_none(dict(trait=trait))
        validate_char_length(dict(trait=trait))
        eq_symbol = "="
        if fuzzy:
            trait = str(cypher_fuzzify(trait))
            eq_symbol = "=~"
        if semmed_triple_id is not None:
            query = queries.Gwas.trait_triple.format(
                trait=trait,
                semmed_triple_id=semmed_triple_id,
                semmed_predicates_clause=semmed_predicates_clause,
                pval_threshold=pval_threshold,
                eq_symbol=eq_symbol,
                limit=limit,
                skip=skip,
            )
        else:
            query = queries.Gwas.trait.format(
                trait=trait,
                semmed_predicates_clause=semmed_predicates_clause,
                pval_threshold=pval_threshold,
                eq_symbol=eq_symbol,
                limit=limit,
                skip=skip,
            )
    res = epigraphdb.run_query(query)
    return res


@router.get("/literature/gwas/pairwise")
def get_literature_gwas_graph(
    trait: Optional[str] = None,
    assoc_trait: Optional[str] = None,
    gwas_id: Optional[str] = None,
    assoc_gwas_id: Optional[str] = None,
    by_gwas_id: bool = False,
    pval_threshold: float = Query(1e-3, ge=0, le=1e-1),
    semmantic_types: List[str] = Query(["nusq"]),
    blacklist: bool = True,
    limit: int = Query(50, ge=1, le=2000),
    skip: int = 0,
    fuzzy: bool = True,
):
    """
    Return information of traits in a Subject-Predicate-Object
    association graph.

    Args:
    - `blacklist` (True) and `semmantic_types`: The list of
    [semmantic types](https://mmtx.nlm.nih.gov/MMTx/semanticTypes.shtml) to exclude (`blacklist`=True) or include (`blacklist`=False).
    Leave `semmantic_types` blank to disable this.
    - `by_gwas_id` (False): If True search by Gwas.id
    - `fuzzy` (True): By default fuzzy match trait name.
    """
    log_args(api="/literature/gwas/pairwise", kwargs=locals())
    if len(semmantic_types) > 0:
        negative = "NOT" if blacklist else ""
        semmantic_type_query = """
          {negative} st.type IN [{types}]
        """.format(
            negative=negative,
            types=",".join([f"'{type}'" for type in semmantic_types]),
        )
    if by_gwas_id:
        validate_at_least_one_not_none(dict(gwas_id=gwas_id))
        if assoc_gwas_id is not None:
            query = queries.GwasPairwise.id_assoc_id.format(
                gwas_id=gwas_id,
                assoc_gwas_id=assoc_gwas_id,
                semmantic_type_query=semmantic_type_query,
                pval_threshold=pval_threshold,
                skip=skip,
                limit=limit,
            )
        else:
            query = queries.GwasPairwise.id.format(
                gwas_id=gwas_id,
                semmantic_type_query=semmantic_type_query,
                pval_threshold=pval_threshold,
                skip=skip,
                limit=limit,
            )
    else:
        validate_at_least_one_not_none(dict(trait=trait))
        validate_char_length(dict(trait=trait, assoc_trait=assoc_trait))
        eq_symbol = "="
        if fuzzy:
            trait = str(cypher_fuzzify(trait))
            assoc_trait = cypher_fuzzify(assoc_trait)
            eq_symbol = "=~"
        if assoc_trait is not None:
            query = queries.GwasPairwise.trait_assoc_trait.format(
                trait=trait,
                assoc_trait=assoc_trait,
                semmantic_type_query=semmantic_type_query,
                pval_threshold=pval_threshold,
                eq_symbol=eq_symbol,
                skip=skip,
                limit=limit,
            )
        else:
            query = queries.GwasPairwise.trait.format(
                trait=trait,
                semmantic_type_query=semmantic_type_query,
                pval_threshold=pval_threshold,
                eq_symbol=eq_symbol,
                skip=skip,
                limit=limit,
            )
    res = epigraphdb.run_query(query)
    return res

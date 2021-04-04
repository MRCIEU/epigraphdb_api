from typing import Optional

from fastapi import APIRouter, Query

from app.settings import epigraphdb
from app.utils import cypher_fuzzify
from app.utils.logging import log_args
from app.utils.validators import (
    validate_at_least_one_not_none,
    validate_char_length,
)

from . import models, queries

router = APIRouter()


@router.get(
    "/ontology/gwas-efo", response_model=models.OntologyGwasEfoResponse
)
def get_ontology_gwas_efo(
    trait: Optional[str] = None,
    efo_term: Optional[str] = None,
    score_threshold: float = Query(0.75, ge=0.0, le=1.0),
    fuzzy: bool = True,
):
    """
    Map Gwas trait to EFO term, via `GWAS_NLP_EFO`
    """
    log_args(api="/ontology/gwas-efo", kwargs=locals())
    validate_at_least_one_not_none(dict(trait=trait, efo_term=efo_term))
    validate_char_length(dict(trait=trait, efo_term=efo_term))
    eq_symbol = "="
    if fuzzy:
        trait = cypher_fuzzify(trait)
        efo_term = cypher_fuzzify(efo_term)
        eq_symbol = "=~"
    if trait is not None and efo_term is not None:
        query = queries.GwasEfo.gwas_efo.format(
            trait=trait,
            efo_term=efo_term,
            score_threshold=score_threshold,
            eq_symbol=eq_symbol,
        )
    elif trait is not None:
        query = queries.GwasEfo.gwas.format(
            trait=trait, score_threshold=score_threshold, eq_symbol=eq_symbol
        )
    elif efo_term is not None:
        query = queries.GwasEfo.efo.format(
            efo_term=efo_term,
            score_threshold=score_threshold,
            eq_symbol=eq_symbol,
        )
    res = epigraphdb.run_query(query)
    return res


@router.get(
    "/ontology/disease-efo", response_model=models.OntologyDiseaseEfoResponse
)
def get_ontology_disease_efo(
    disease_label: Optional[str] = None,
    efo_term: Optional[str] = None,
    fuzzy: bool = True,
):
    """
    Map Disease label to EFO term, via `MONDO_MAP_EFO`
    """
    log_args(api="/ontology/disease-efo", kwargs=locals())
    validate_at_least_one_not_none(
        dict(disease_label=disease_label, efo_term=efo_term)
    )
    validate_char_length(dict(disease_label=disease_label, efo_term=efo_term))
    eq_symbol = "="
    if fuzzy:
        disease_label = cypher_fuzzify(disease_label)
        efo_term = cypher_fuzzify(efo_term)
        eq_symbol = "=~"
    if disease_label is not None and efo_term is not None:
        query = queries.DiseaseEfo.disease_efo.format(
            disease_label=disease_label, efo_term=efo_term, eq_symbol=eq_symbol
        )
    elif disease_label is not None:
        query = queries.DiseaseEfo.disease.format(
            disease_label=disease_label, eq_symbol=eq_symbol
        )
    elif efo_term is not None:
        query = queries.DiseaseEfo.efo.format(
            efo_term=efo_term, eq_symbol=eq_symbol
        )
    res = epigraphdb.run_query(query)
    return res


@router.get(
    "/ontology/gwas-efo-disease",
    response_model=models.OntologyGwasEfoDiseaseResponse,
)
def get_ontology_gwas_efo_disease(
    trait: Optional[str] = None,
    efo_term: Optional[str] = None,
    disease_label: Optional[str] = None,
    score_threshold: float = Query(0.75, ge=0.0, le=1.0),
    fuzzy: bool = True,
):
    """
    Map Gwas trait to Disease label, via Efo term.
    """
    log_args(api="/ontology/gwas-efo-disease", kwargs=locals())
    validate_at_least_one_not_none(
        dict(trait=trait, disease_label=disease_label, efo_term=efo_term)
    )
    validate_char_length(
        dict(trait=trait, disease_label=disease_label, efo_term=efo_term)
    )
    eq_symbol = "="
    if fuzzy:
        trait = cypher_fuzzify(trait)
        efo_term = cypher_fuzzify(efo_term)
        disease_label = cypher_fuzzify(disease_label)
        eq_symbol = "=~"
    if (
        trait is not None
        and disease_label is not None
        and efo_term is not None
    ):
        query = queries.GwasEfoDisease.gwas_efo_disease.format(
            trait=trait,
            efo_term=efo_term,
            disease_label=disease_label,
            score_threshold=score_threshold,
            eq_symbol=eq_symbol,
        )
    elif trait is not None and efo_term is not None:
        query = queries.GwasEfoDisease.gwas_efo.format(
            trait=trait,
            efo_term=efo_term,
            score_threshold=score_threshold,
            eq_symbol=eq_symbol,
        )
    elif efo_term is not None and disease_label is not None:
        query = queries.GwasEfoDisease.efo_disease.format(
            efo_term=efo_term,
            disease_label=disease_label,
            score_threshold=score_threshold,
            eq_symbol=eq_symbol,
        )
    elif trait is not None and disease_label is not None:
        query = queries.GwasEfoDisease.gwas_disease.format(
            trait=trait,
            disease_label=disease_label,
            score_threshold=score_threshold,
            eq_symbol=eq_symbol,
        )
    elif trait is not None:
        query = queries.GwasEfoDisease.gwas.format(
            trait=trait, score_threshold=score_threshold, eq_symbol=eq_symbol
        )
    elif efo_term is not None:
        query = queries.GwasEfoDisease.efo.format(
            efo_term=efo_term,
            score_threshold=score_threshold,
            eq_symbol=eq_symbol,
        )
    elif disease_label is not None:
        query = queries.GwasEfoDisease.disease.format(
            disease_label=disease_label,
            score_threshold=score_threshold,
            eq_symbol=eq_symbol,
        )
    res = epigraphdb.run_query(query)
    return res

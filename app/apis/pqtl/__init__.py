import warnings
from enum import Enum
from typing import Union

from fastapi import APIRouter, Query

from app.settings import pqtl
from app.utils.logging import log_args
from app.utils.process_query import format_response

from .models import (
    ListPQTLResponse,
    PQTLPleioCountResponse,
    PQTLPleioProteinsResponse,
    PQTLResponse,
)
from .queries import NonProteins, Pleio, Proteins

router = APIRouter()
summary = "Returns the MR and other results related to pQTL"
summary_pleio = (
    "Returns the number or the list of associated proteins in the database"
)
summary_list = (
    "Returns either the list of all proteins or traits in the database"
)


class RtypeInput(str, Enum):
    simple = "simple"
    mrres = "mrres"
    sglmr = "sglmr"
    inst = "inst"
    sense = "sense"


class SearchflagInput(str, Enum):
    proteins = "proteins"
    traits = "traits"


class ListFlagInput(str, Enum):
    outcomes = "outcomes"
    exposures = "exposures"


class PrflagInput(str, Enum):
    # NOTE: use _count instead of count as mypy
    #       throws error: is count a reserved method?
    _count = "count"
    proteins = "proteins"


@router.get("/pqtl/", response_model=PQTLResponse)
def get_pqtl(
    query: str,
    rtype: RtypeInput,
    searchflag: SearchflagInput,
    pvalue: float = Query(0.5, ge=0.0, le=1.0),
):

    """Returns the MR and other results related to pQTL

    - `query`: Protein or trait name e.g., ADAM19 or Inflammatory bowel disease
    - `rtype`: Results type
      - "simple": Basic summary,
      - "mrres": MR results,
      - "sglmr": Single SNP MR results,
      - "inst": SNP information,
      - "sense": Sensitivity analysis,
    - pvalue: MR pvalue threshold
    - searchflag:
      - "proteins": Searches for a protein e.g., if query=ADAM19
      - "traits": Searches for a specific trait e.g.,
        if query=Inflammatory bowel disease
    """
    log_args(api="/pqtl/", kwargs=locals())
    data = querypqtl(query, rtype.value, pvalue, searchflag.value)
    return data


@router.get(
    "/pqtl/pleio/",
    response_model=Union[PQTLPleioProteinsResponse, PQTLPleioCountResponse],
)
def get_pqtl_pleio(rsid: str, prflag: PrflagInput):

    """Returns the number or the list of associated proteins in the database

    - `rsid`: SNP rs_ID e.g., rs1260326
    - `prflag`:
      - "count"
      - "proteins"
    """
    log_args(api="/pqtl/pleio/", kwargs=locals())
    data = calc_flag_pleio(rsid, prflag.value)
    return data


@router.get("/pqtl/list/", response_model=ListPQTLResponse)
def get_pqtl_list(flag: ListFlagInput):
    """Returns either the list of all proteins or traits in the database

    "searchable_entities": {"flag": "Search for 'outcomes' or 'exposures'"}

    """
    log_args(api="/pqtl/list/", kwargs=locals())

    data = pQTL_list(flag.value)
    return data


def querypqtl(query: str, rtype: str, pvalue: float, searchflag: str):
    """Returns the table of results as per
    the DB "query", data type "rtype",
    pvalue threshold "pvalue" and search type (either proteins or traits)

    Args:
      query: str:
      rtype: str:
      pvalue: float:
      searchflag: str:

    Returns:

    """
    if searchflag in ("proteins", "traits"):
        if searchflag == "proteins":
            if rtype in ["simple", "mrres", "sglmr", "inst", "sense"]:
                query = getattr(Proteins, rtype).format(
                    query=query, pvalue=pvalue
                )
            else:
                query = ""
        else:
            if rtype in ["simple", "mrres", "sglmr", "inst", "sense"]:
                query = getattr(NonProteins, rtype).format(
                    query=query, pvalue=pvalue
                )
            else:
                query = ""
    else:
        query = ""
    if query:
        data = pqtl.run_query(query, format=False)
    else:
        data = {}
        warnings.simplefilter("always")
        warnings.warn("Invalid user input. No query was generated.")
    response = format_response(data, query)
    return response


def calc_flag_pleio(rsid: str, prflag: str):
    """calc_flag_pleio : returns either
    the number of associated proteins with a SNP (rsid) and prflag = "count" or
    the list of associated proteins in all other cases.

    Args:
      rsid: str:
      prflag: str:

    Returns:

    """
    if prflag == "count":
        ptcount = 0
        query = Pleio.count.format(rsid=rsid)
        data = pqtl.run_query(query, format=False)
        for row in data:
            ptcount = row["pt_count"]
        # metadata = {"query": trim_cypher_query(query)}
        out = {"metadata": None, "results": ptcount}
    elif prflag == "proteins":
        query = Pleio.non_count.format(rsid=rsid)
        data = pqtl.run_query(query, format=False)
        out = format_response(data, query)
    else:
        query = ""
        data = {}
        out = format_response(data, query)
        warnings.simplefilter("always")
        warnings.warn("Invalid user input. No query was generated.")
    return out


def pQTL_list(flag: str):
    """pQTL_list : returns the list of proteins or outcomes

    Args:
      flag: str:

    Returns:

    """
    if flag == "outcomes":
        query = "match (o:Outcome) return distinct o.outID as outID;"
    elif flag == "exposures":
        query = "match (e:Exposure) return distinct e.expID as expID;"
    else:
        query = ""
    if query:
        data = pqtl.run_query(query, format=False)
    else:
        data = {}
        warnings.simplefilter("always")
        warnings.warn("Invalid user input. No query was generated.")
    response = format_response(data, query)
    return response

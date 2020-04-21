from pprint import pformat

from fastapi import APIRouter, FastAPI
from starlette.staticfiles import StaticFiles

from app import settings
from app.resources.info import description, title, version
from app.utils.logging import logger  # noqa:F401

from .apis import (
    confounder,
    covid_xqtl,
    cypher,
    drugs,
    gene,
    genetic_cor,
    literature,
    mappings,
    meta,
    mr,
    obs_cor,
    ontology,
    pathway,
    pqtl,
    protein,
    prs,
    raw_cypher,
    status,
    top,
    xqtl,
)

app = FastAPI(
    title=title, description=description, version=version, docs_url="/"
)
app.mount("/static", StaticFiles(directory="static"))

top_router = APIRouter()

logger.info(pformat(settings.env_configs))


# ==== Endpoints ====
app.include_router(top.router, tags=["status"])
# private
if settings.api_private_access:
    app.include_router(status.router, tags=["private: status"])
    # raw cypher
    app.include_router(raw_cypher.router, tags=["cypher"])
# topics
app.include_router(mr.router, tags=["topics"])
app.include_router(genetic_cor.router, tags=["topics"])
app.include_router(obs_cor.router, tags=["topics"])
app.include_router(confounder.router, tags=["topics"])
app.include_router(pathway.router, tags=["topics"])
app.include_router(drugs.router, tags=["topics", "drugs"])
app.include_router(xqtl.router, tags=["topics", "xqtl"])
app.include_router(prs.router, tags=["topics"])
app.include_router(pqtl.router, tags=["topics", "pqtl"])
app.include_router(literature.router, tags=["topics", "literature"])
app.include_router(meta.router, tags=["metadata"])
app.include_router(cypher.router, tags=["cypher"])
app.include_router(ontology.router, tags=["topics", "ontology"])
app.include_router(protein.router, tags=["topics", "protein"])
app.include_router(gene.router, tags=["topics", "gene"])
# utils
app.include_router(mappings.router, tags=["mappings"])

# hype
app.include_router(covid_xqtl.router, tags=["covid-19"])

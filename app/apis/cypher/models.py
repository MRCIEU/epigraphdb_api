from typing import List

from pydantic import BaseModel, validator

from app.models.api_meta_graph import (
    EpigraphdbMetaNodesFull,
    EpigraphdbMetaRels,
)
from app.models.schema_meta_rels import meta_path_schema

cypher_builder_limit_threshold = 1000


class CypherRequest(BaseModel):
    query: str


class CypherBuilderRequest(BaseModel):
    source_meta_node: EpigraphdbMetaNodesFull
    target_meta_node: EpigraphdbMetaNodesFull
    meta_rel: EpigraphdbMetaRels
    where: List[str] = []
    order_by: List[str] = []
    limit: int = 100

    @validator("limit")
    def validate_limit(cls, v):
        if v < 0 or v > cypher_builder_limit_threshold:
            raise ValueError(
                f"Exceeds limit [0, {cypher_builder_limit_threshold}]"
            )
        return v

    @validator("order_by")
    def validate_order_by(cls, v, values):
        if len(v) > 0 and len(values.get("where")) == 0:
            raise ValueError(
                f"You must specify valid where clause(s) to use order_by"
            )
        return v

    @validator("meta_rel")
    def validate_schema(cls, v, values):
        meta_path = meta_path_schema[v]
        if meta_path[0] != values.get("source_meta_node") or meta_path[
            1
        ] != values.get("target_meta_node"):
            raise ValueError(
                "Path does not exists. Check EpiGraphDB schema for valid paths."
            )
        return v

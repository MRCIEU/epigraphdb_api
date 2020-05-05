from typing import List, Union

from pydantic import BaseModel

from app.models import ApiMetadata
from app.models.output_nodes import DrugItem, GeneItem
from app.models.output_rels import CpicItem, OpentargetsDrugToTargetItem


class GeneDrugsResultItem(BaseModel):

    gene: GeneItem
    drug: DrugItem
    r: Union[OpentargetsDrugToTargetItem, CpicItem]
    r_source: str


class GeneDrugsResponse(BaseModel):

    metadata: ApiMetadata
    results: List[GeneDrugsResultItem]

from typing import List

from pydantic import BaseModel


class PpiRequest(BaseModel):
    uniprot_id_list: List[str]


class PpiGraphRequest(BaseModel):
    uniprot_id_list: List[str]
    n_intermediate_proteins: int = 0


class PathwayRequest(BaseModel):
    uniprot_id_list: List[str]

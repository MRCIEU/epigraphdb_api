from typing import List

from pydantic import BaseModel


class GeneToProteinRequest(BaseModel):
    gene_name_list: List[str]

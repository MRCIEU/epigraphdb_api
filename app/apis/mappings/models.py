from typing import List, Optional

from pydantic import BaseModel


class GeneToProteinRequest(BaseModel):
    gene_name_list: Optional[List[str]] = None
    gene_id_list: Optional[List[str]] = None
    by_gene_id: bool = False

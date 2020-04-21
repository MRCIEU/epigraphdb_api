from typing import List

# NOTE: semmed is a special node and not supposed to be
#       searched for now
epigraphdb_meta_nodes = {
    "Disease": {"id": "id", "name": "label"},
    "Drug": {"id": "label", "name": "label"},
    "Efo": {"id": "id", "name": "value"},
    "Event": {"id": "reactome_id", "name": "name"},
    "Gene": {"id": "ensembl_id", "name": "name"},
    "Gtex": {"id": "tissue", "name": "tissue"},
    "Gwas": {"id": "id", "name": "trait"},
    "Literature": {"id": "pubmed_id", "name": "pubmed_id"},
    "Pathway": {"id": "reactome_id", "name": "name"},
    "Protein": {"id": "uniprot_id", "name": "uniprot_id"},
    "SemmedTerm": {"id": "id", "name": "name"},
    "Variant": {"id": "name", "name": "name"},
}

epigraphdb_meta_node_black_list: List[str] = ["Meta", "SemmedTriple"]

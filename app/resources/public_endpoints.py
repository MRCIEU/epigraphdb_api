from typing import Any, Callable, Dict, List, Optional

from typing_extensions import TypedDict

from app.apis import (
    covid_xqtl,
    cypher,
    gene,
    literature,
    meta,
    opengwas,
    xqtl_trans_ancestry_pwas,
)
from app.apis.confounder import get_confounder
from app.apis.drugs import get_drugs_risk_factors
from app.apis.genetic_cor import get_genetic_cor
from app.apis.mappings import post_gene_to_protein
from app.apis.mr import get_mr
from app.apis.nlp import (
    get_nlp_query_ent,
    get_nlp_query_ent_encode,
    get_nlp_query_text,
)
from app.apis.obs_cor import get_obs_cor
from app.apis.ontology import (
    get_ontology_disease_efo,
    get_ontology_gwas_efo,
    get_ontology_gwas_efo_disease,
)
from app.apis.pathway import get_pathway
from app.apis.pqtl import get_pqtl, get_pqtl_list, get_pqtl_pleio
from app.apis.protein import (
    post_protein_pathway,
    post_protein_ppi,
    post_protein_ppi_graph,
)
from app.apis.prs import get_prs
from app.apis.top import get_top_ping
from app.apis.xqtl import (
    get_xqtl_multi_snp_mr,
    get_xqtl_single_snp_mr,
    post_xqtl_gene_by_variant,
)


class EndpointExample(TypedDict, total=False):
    desc: str
    endpoint: str
    params: Optional[Dict[str, Any]]


class EndpointData(TypedDict):
    func: Callable
    tests: List[EndpointExample]


topic_params: Dict[str, EndpointData] = {
    "GET /mr": {
        "func": get_mr,
        "tests": [
            {
                "desc": "Query for exposure trait",
                "params": {"exposure_trait": "Body mass index"},
            },
            {
                "desc": "Query for outcome trait",
                "params": {"outcome_trait": "Body mass index"},
            },
            {
                "desc": "Query for both exposure and outcome",
                "params": {
                    "expsoure_trait": "Body mass index",
                    "outcome_trait": "Coronary heart disease",
                },
            },
        ],
    },
    "GET /obs-cor": {
        "func": get_obs_cor,
        "tests": [
            {"params": {"trait": "Waist circumference"}},
            {
                "desc": "Adjust for correlation coefficient",
                "params": {
                    "trait": "Waist circumference",
                    "cor_coef_threshold": 0.2,
                },
            },
        ],
    },
    "GET /genetic-cor": {
        "func": get_genetic_cor,
        "tests": [
            {"params": {"trait": "Waist circumference"}},
            {
                "desc": "Adjust for correlation coefficient",
                "params": {
                    "trait": "Waist circumference",
                    "cor_coef_threshold": 0.2,
                },
            },
        ],
    },
    "GET /confounder": {
        "func": get_confounder,
        "tests": [
            {
                "desc": "Confounder (default)",
                "params": {
                    "exposure_trait": "Body mass index",
                    "outcome_trait": "Coronary heart disease",
                },
            },
            {
                "desc": "Intermediate",
                "params": {
                    "exposure_trait": "Body mass index",
                    "outcome_trait": "Coronary heart disease",
                    "type": "intermediate",
                },
            },
            {
                "desc": "Reverse intermediate",
                "params": {
                    "exposure_trait": "Body mass index",
                    "outcome_trait": "Coronary heart disease",
                    "type": "reverse_intermediate",
                },
            },
            {
                "desc": "Collider",
                "params": {
                    "exposure_trait": "Body mass index",
                    "outcome_trait": "Coronary heart disease",
                    "type": "collider",
                },
            },
        ],
    },
    "GET /drugs/risk-factors": {
        "func": get_drugs_risk_factors,
        "tests": [{"params": {"trait": "Coronary heart disease"}}],
    },
    "GET /pathway": {
        "func": get_pathway,
        "tests": [{"params": {"trait": "LDL cholesterol"}}],
    },
    "GET /xqtl/multi-snp-mr": {
        "func": get_xqtl_multi_snp_mr,
        "tests": [
            {
                "desc": "Query by exposure gene",
                "params": {"exposure_gene": "PLAU"},
            },
            {
                "desc": "Query by outcome trait",
                "params": {"outcome_trait": "Crohn's disease"},
            },
        ],
    },
    "GET /xqtl/single-snp-mr": {
        "func": get_xqtl_single_snp_mr,
        "tests": [
            {
                "desc": "Query by exposure gene",
                "params": {"exposure_gene": "PLAU"},
            },
            {
                "desc": "Query by outcome trait",
                "params": {"outcome_trait": "Crohn's disease"},
            },
            {"desc": "Query by variant", "params": {"variant": "rs1250566"}},
        ],
    },
    "POST /xqtl/single-snp-mr/gene-by-variant": {
        "func": post_xqtl_gene_by_variant,
        "tests": [{"params": {"variant_list": ["rs9272544", "rs242797"]}}],
    },
    "GET /prs": {
        "func": get_prs,
        "tests": [{"params": {"trait": "Body mass index"}}],
    },
    "POST /protein/ppi": {
        "func": post_protein_ppi,
        "tests": [
            {"params": {"uniprot_id_list": ["P30793", "Q9NZM1", "O95236"]}}
        ],
    },
    "POST /protein/ppi/pairwise": {
        "func": post_protein_ppi_graph,
        "tests": [
            {
                "desc": "Default query (direct interaction)",
                "params": {
                    "uniprot_id_list": [
                        "P30793",
                        "Q9NZM1",
                        "O95236",
                        "P32456",
                        "Q13536",
                        "Q9NRQ5",
                        "O60674",
                        "O14933",
                        "P32455",
                        "P40306",
                        "P42224",
                        "P28838",
                        "P23381",
                    ]
                },
            },
            {
                "desc": "With at most `1` intermediate protein",
                "params": {
                    "uniprot_id_list": [
                        "P30793",
                        "Q9NZM1",
                        "O95236",
                        "P32456",
                        "Q13536",
                        "Q9NRQ5",
                        "O60674",
                        "O14933",
                        "P32455",
                        "P40306",
                        "P42224",
                        "P28838",
                        "P23381",
                    ],
                    "n_intermediate_proteins": 1,
                },
            },
        ],
    },
    "POST /protein/in-pathway": {
        "func": post_protein_pathway,
        "tests": [
            {"params": {"uniprot_id_list": ["O14933", "O60674", "P32455"]}}
        ],
    },
    "GET /gene/druggability/ppi": {
        "func": gene.get_gene_druggability_ppi,
        "tests": [{"params": {"gene_name": "IL23R"}}],
    },
    "GET /gene/literature": {
        "func": gene.get_gene_literature,
        "tests": [
            {
                "params": {
                    "gene_name": "IL23R",
                    "object_name": "Inflammatory Bowel Diseases",
                }
            }
        ],
    },
    "GET /gene/drugs": {
        "func": gene.get_gene_drugs,
        "tests": [{"params": {"gene_name": "TFRC"}}],
    },
    "GET /ontology/gwas-efo": {
        "func": get_ontology_gwas_efo,
        "tests": [
            {
                "desc": "Default (fuzzy matching)",
                "params": {"trait": "body mass", "efo_term": "body mass"},
            },
            {
                "desc": "Exact matching",
                "params": {"trait": "Body mass index", "fuzzy": False},
            },
        ],
    },
    "GET /ontology/disease-efo": {
        "func": get_ontology_disease_efo,
        "tests": [
            {"params": {"disease_label": "leukemia", "efo_term": "leukemia"}}
        ],
    },
    "GET /ontology/gwas-efo-disease": {
        "func": get_ontology_gwas_efo_disease,
        "tests": [
            {
                "desc": "By trait and disease_label",
                "params": {
                    "trait": "infectious disease",
                    "disease_label": "infectious disease",
                    "score_threshold": 0.70,
                },
            },
            {
                "desc": "By trait and efo_term",
                "params": {
                    "trait": "insomnia",
                    "efo_term": "insomnia",
                    "score_threshold": 0.70,
                },
            },
            {
                "desc": "By efo_term and disease_label",
                "params": {
                    "efo_term": "insomnia",
                    "disease_label": "insomnia",
                    "score_threshold": 0.70,
                },
            },
        ],
    },
    "GET /literature/gene": {
        "func": literature.get_gene_literature,
        "tests": [
            {
                "params": {
                    "gene_name": "IL23R",
                    "object_name": "Inflammatory bowel disease",
                }
            }
        ],
    },
    "GET /literature/gwas": {
        "func": literature.get_literature_gwas_semmed,
        "tests": [
            {
                "desc": "Search by trait name",
                "params": {"trait": "Sleep duration", "fuzzy": False},
            },
            {
                "desc": "Search by id",
                "params": {"gwas_id": "ieu-a-1088", "by_gwas_id": True},
            },
            {
                "desc": "Search by id and semmed triple id",
                "params": {
                    "gwas_id": "ieu-a-1088",
                    "semmed_triple_id": "C0060135:INTERACTS_WITH:C0001962",
                    "by_gwas_id": True,
                },
            },
            {
                "desc": "Search by trait name and filter predicate",
                "params": {
                    "trait": "Sleep duration",
                    "semmed_predicates": ["COEXISTS_WITH", "TREATS"],
                    "fuzzy": False,
                },
            },
        ],
    },
    "GET /literature/gwas/pairwise": {
        "func": literature.get_literature_gwas_graph,
        "tests": [
            {
                "desc": "Search by trait name",
                "params": {
                    "trait": "Sleep duration",
                    "assoc_trait": "Coronary heart disease",
                    "pval_threshold": 1e-1,
                    "blacklist": True,
                    "semmantic_types": ["nusq", "dsyn"],
                    "limit": 10,
                    "fuzzy": True,
                },
            },
            {
                "desc": "Search by Gwas.id",
                "params": {
                    "gwas_id": "ieu-a-1088",
                    "assoc_gwas_id": "ieu-a-6",
                    "by_gwas_id": True,
                    "pval_threshold": 1e-1,
                    "blacklist": True,
                    "semmantic_types": ["nusq", "dsyn"],
                    "limit": 10,
                    "fuzzy": False,
                },
            },
            {
                "desc": "Whitelist semmantic types",
                "params": {
                    "gwas_id": "ieu-a-1088",
                    "assoc_gwas_id": "ieu-a-6",
                    "by_gwas_id": True,
                    "pval_threshold": 1e-1,
                    "blacklist": False,
                    "semmantic_types": ["aapp", "orch"],
                    "limit": 10,
                    "fuzzy": False,
                },
            },
        ],
    },
    "GET /pqtl/": {
        "func": get_pqtl,
        "tests": [
            {
                "desc": "Search protein",
                "params": {
                    "query": "ADAM15",
                    "rtype": "simple",
                    "searchflag": "proteins",
                },
            },
            {
                "desc": "Search trait",
                "params": {
                    "query": "Coronary heart disease",
                    "rtype": "simple",
                    "searchflag": "traits",
                },
            },
        ],
    },
    "GET /pqtl/pleio/": {
        "func": get_pqtl_pleio,
        "tests": [{"params": {"rsid": "rs1260326", "prflag": "proteins"}}],
    },
    "GET /pqtl/list/": {
        "func": get_pqtl_list,
        "tests": [
            {"desc": "List outcomes", "params": {"flag": "outcomes"}},
            {"desc": "List exposures", "params": {"flag": "exposures"}},
        ],
    },
    "GET /covid-19/ctda/list/{entity}": {
        "func": covid_xqtl.get_list_gwas,
        "tests": [
            {
                "desc": "List exposure genes",
                "endpoint": "GET /covid-19/ctda/list/gene",
                "params": None,
            },
            {
                "desc": "List outcome gwas",
                "endpoint": "GET /covid-19/ctda/list/gwas",
                "params": None,
            },
            {
                "desc": "List tissues",
                "endpoint": "GET /covid-19/ctda/list/tissue",
                "params": None,
            },
        ],
    },
    "GET /covid-19/ctda/single-snp-mr/{entity}": {
        "func": covid_xqtl.get_single_snp_mr,
        "tests": [
            {
                "desc": "By exposure gene",
                "endpoint": "GET /covid-19/ctda/single-snp-mr/gene",
                "params": {"q": "ENSG00000102967"},
            },
            {
                "desc": "By outcome gwas",
                "endpoint": "GET /covid-19/ctda/single-snp-mr/gwas",
                "params": {"q": "7", "pval_threshold": 1e-2},
            },
            {
                "desc": "By tissue",
                "endpoint": "GET /covid-19/ctda/single-snp-mr/tissue",
                "params": {"q": "Lung"},
            },
        ],
    },
    "GET /covid-19/ctda/multi-snp-mr/{entity}": {
        "func": covid_xqtl.get_multi_snp_mr,
        "tests": [
            {
                "desc": "By exposure gene",
                "endpoint": "GET /covid-19/ctda/multi-snp-mr/gene",
                "params": {"q": "ENSG00000102967"},
            },
            {
                "desc": "By outcome gwas",
                "endpoint": "GET /covid-19/ctda/multi-snp-mr/gwas",
                "params": {"q": "7", "pval_threshold": 1e-2},
            },
            {
                "desc": "By tissue",
                "endpoint": "GET /covid-19/ctda/multi-snp-mr/tissue",
                "params": {"q": "Lung"},
            },
        ],
    },
    "GET /xqtl_trans_ancestry_pwas/{entity}": {
        "func": xqtl_trans_ancestry_pwas.list_ents,
        "tests": [
            {
                "desc": "Get list of GWAS envolved in the study",
                "endpoint": "GET /xqtl_trans_ancestry_pwas/gwas",
                "params": None,
            },
            {
                "desc": "Get list of genes envolved in the study",
                "endpoint": "GET /xqtl_trans_ancestry_pwas/gene",
                "params": None,
            },
        ],
    },
    "GET /xqtl_trans_ancestry_pwas/xqtl_pwas_mr/{entity}": {
        "func": xqtl_trans_ancestry_pwas.xqtl_pwas_mr,
        "tests": [
            {
                "desc": "Query study results by GWAS",
                "endpoint": "GET /xqtl_trans_ancestry_pwas/xqtl_pwas_mr/gwas",
                "params": {"q": "gbmi-a-00001-nfe-b", "pval_threshold": 1e-2},
            },
            {
                "desc": "Query study results by gene",
                "endpoint": "GET /xqtl_trans_ancestry_pwas/xqtl_pwas_mr/gene",
                "params": {"q": "ENSG00000168685", "pval_threshold": 1e-2},
            },
        ],
    },
    "GET /opengwas/search/id": {
        "func": opengwas.get_gwas_recommender,
        "tests": [
            {
                "desc": "Recommend OpenGWAS datasets by id, ieu-a-2",
                "endpoint": "GET /opengwas/search/id",
                "params": {"gwas_id": "ieu-a-2"},
            },
            {
                "desc": "Recommend OpenGWAS datasets by id, ieu-a-10",
                "endpoint": "GET /opengwas/search/id",
                "params": {"gwas_id": "ieu-a-10"},
            },
        ],
    },
}

util_params: Dict[str, EndpointData] = {
    "GET /ping": {
        "func": get_top_ping,
        "tests": [{"desc": "Default", "params": None}],
    },
    "GET /meta/schema": {
        "func": meta.get_schema,
        "tests": [
            {"desc": "Default", "params": {"graphviz": False, "plot": False}},
            {
                "desc": "Graphviz format",
                "params": {"graphviz": True, "plot": False},
            },
        ],
    },
    "GET /meta/nodes/list": {
        "func": meta.meta_nodes_list,
        "tests": [{"params": None}],
    },
    "GET /meta/nodes/id-name-schema": {
        "func": meta.meta_nodes_id_name_schema,
        "tests": [{"params": None}],
    },
    "GET /meta/rels/list": {
        "func": meta.meta_rels_list,
        "tests": [{"params": None}],
    },
    "GET /meta/nodes/{meta_node}/list": {
        "func": meta.nodes_list,
        "tests": [
            {
                "endpoint": "GET /meta/nodes/Gwas/list",
                "desc": "List Gwas nodes (only id and name)",
                "params": {"full_data": False, "limit": 5},
            },
            {
                "endpoint": "GET /meta/nodes/Gwas/list",
                "desc": "List Gwas nodes (full data)",
                "params": {"full_data": True, "limit": 5},
            },
        ],
    },
    "GET /meta/nodes/{meta_node}/search": {
        "func": meta.nodes_search,
        "tests": [
            {
                "endpoint": "GET /meta/nodes/Gwas/search",
                "desc": "Search Gwas nodes by id",
                "params": {"id": "ieu-a-2"},
            },
            {
                "endpoint": "GET /meta/nodes/Gwas/search",
                "desc": "Search Gwas nodes by name",
                "params": {"name": "body mass"},
            },
        ],
    },
    "GET /meta/nodes/{meta_node}/search-neighbour": {
        "func": meta.nodes_search_neighbour,
        "tests": [
            {
                "endpoint": "GET /meta/nodes/Gwas/search-neighbour",
                "desc": "Search neighbour nodes of a Gwas node",
                "params": {"id": "ieu-a-2"},
            }
        ],
    },
    "GET /meta/rels/{meta_rel}/list": {
        "func": meta.rels_list,
        "tests": [
            {
                "endpoint": "GET /meta/rels/MR_EVE_MR/list",
                "desc": "List MR (MR EvE) relationships",
                "params": None,
            }
        ],
    },
    "GET /meta/paths/search": {
        "func": meta.get_paths_search,
        "tests": [
            {
                "desc": "Search pair-wise rels between two Gwas",
                "params": {
                    "meta_node_source": "Gwas",
                    "meta_node_target": "Gwas",
                    "id_source": "ieu-a-2",
                    "id_target": "ieu-a-10",
                    "max_path_length": 1,
                    "limit": 3,
                },
            }
        ],
    },
    "POST /mappings/gene-to-protein": {
        "func": post_gene_to_protein,
        "tests": [
            {
                "desc": "(default) By HGNC symbols",
                "params": {"gene_name_list": ["GCH1", "MYOF"]},
            },
            {
                "desc": "By Ensembl IDs",
                "params": {
                    "gene_id_list": ["ENSG00000162594", "ENSG00000113302"],
                    "by_gene_id": True,
                },
            },
        ],
    },
    "GET /nlp/query/text": {
        "func": get_nlp_query_text,
        "tests": [
            {
                "params": {
                    "text": "Coronary heart disease",
                    "asis": True,
                    "include_meta_nodes": ["Gwas", "Disease"],
                    "limit": 10,
                }
            }
        ],
    },
    "GET /nlp/query/entity": {
        "func": get_nlp_query_ent,
        "tests": [
            {
                "params": {
                    "entity_id": "ieu-a-2",
                    "meta_node": "Gwas",
                    "include_meta_nodes": ["Efo"],
                    "limit": 5,
                }
            }
        ],
    },
    "GET /nlp/query/entity/encode": {
        "func": get_nlp_query_ent_encode,
        "tests": [
            {
                "params": {
                    "entity_id": "ieu-a-2",
                    "meta_node": "Gwas",
                }
            }
        ],
    },
    "POST /cypher": {
        "func": cypher.post_cypher,
        "tests": [
            {
                "params": {
                    "query": " ".join(
                        """
                        MATCH (n:Gwas)-[r:MR_EVE_MR]-(m:Gwas)
                        WHERE r.pval < 1e-5
                        RETURN properties(n), properties(r), properties(m)
                        LIMIT 10
                    """.replace(
                            "\n", " "
                        ).split()
                    )
                }
            }
        ],
    },
}

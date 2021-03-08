class Ppi:
    query = """
        MATCH
            p=(protein:Protein)-[r:STRING_INTERACT_WITH]-(assoc_protein:Protein)
        WHERE
            protein.uniprot_id IN {protein_list}
        RETURN
            protein {{.uniprot_id}},
            assoc_protein {{.uniprot_id}}
    """
    graph = """
        MATCH
            p=(protein:Protein)-[r:STRING_INTERACT_WITH*1..{n}]-(assoc_protein:Protein)
        WHERE
            protein.uniprot_id IN {protein_list} AND
            assoc_protein.uniprot_id IN {protein_list}
        RETURN
            protein.uniprot_id AS protein,
            assoc_protein.uniprot_id AS assoc_protein,
            length(p) AS path_size
        """


class Pathway:
    query = """
      MATCH
          p=(protein:Protein)-[r:PROTEIN_IN_PATHWAY]-(pathway:Pathway)
          WHERE
              protein.uniprot_id IN {protein_list}
          RETURN
              protein.uniprot_id AS uniprot_id,
              count(p) AS pathway_count,
              collect(pathway.id) AS pathway_reactome_id
      """

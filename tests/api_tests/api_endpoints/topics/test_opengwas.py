import pytest

from app.apis.opengwas import (
    _search_by_embeddings,
    _search_by_text,
    get_gwas_recommender,
)

test_studies = [
    ("ieu-a-2"),
    ("ieu-a-10"),
]


@pytest.mark.parametrize("gwas_id", test_studies)
def test_get_gwas_recommender(gwas_id):
    results = get_gwas_recommender(gwas_id=gwas_id, limit=5)
    assert len(results["results"]) > 0


@pytest.mark.parametrize("gwas_id", test_studies)
def test_embeddings(gwas_id):
    results = _search_by_embeddings(gwas_id=gwas_id, limit=5)
    assert len(results) > 0


@pytest.mark.parametrize("gwas_id", test_studies)
def test_text(gwas_id):
    results = _search_by_text(gwas_id=gwas_id, limit=5)
    assert len(results) > 0

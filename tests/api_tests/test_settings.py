from app.settings import epigraphdb, pqtl


def test_epigraphdb_running():
    assert epigraphdb.check_connection()


def test_pqtl_running():
    assert pqtl.check_connection()

from app import settings
from app.resources._global import get_service_builds

builds = get_service_builds()

title = "EpiGraphDB API"
description = f"""<a style="color:#757575">A RESTful Web API for querying EpiGraphDB.</a>

**Service builds**:
- EpiGraphDB: `{builds["epigraphdb"]["overall"]}`
    - Database: `{builds["epigraphdb"]["database"]}`
    - API: `{builds["epigraphdb"]["api"]}`
- pQTL database: `{builds["pqtl"]}`
"""
# if settings.api_private_access:
#     # FIXME:  git info will not work in submodule
#     # git_info = get_git_info()
#     description += textwrap.dedent(
#         f"""
#     **Links**:
#     - private: [EpiGraphDB Neo4j Browser]({settings.epigraphdb_browser})
#     """
#     )
version = settings.api_version

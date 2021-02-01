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

Visit the
[API endpoints page](
http://docs.epigraphdb.org/api/api-endpoints/
)
in the EpiGraphDB documentation for
further information.
"""
version = settings.api_version

"""
Control and configure global settings.
"""
from pathlib import Path

from app.utils.database import Neo4jDB
from epigraphdb_common_utils.api_env_configs import env_configs

# General config
epigraphdb_version = env_configs["epigraphdb_db_version"]
api_version = "1.0"
api_private_access = env_configs["api_private_access"]
if api_private_access:
    api_version = f"{api_version}-private"

api_key = env_configs["api_key"]

# directories
log_dir = Path("/tmp/epigraphdb_api/logs")
cache_dir = Path("/tmp/epigraphdb_api/cache")
log_dir.mkdir(parents=True, exist_ok=True)
cache_dir.mkdir(parents=True, exist_ok=True)

# EpiGraphDB database
epigraphdb = Neo4jDB(
    hostname=env_configs["epigraphdb_server"],
    bolt_port=env_configs["epigraphdb_port"],
    user=env_configs["epigraphdb_user"],
    password=env_configs["epigraphdb_passwd"],
    version=env_configs["epigraphdb_db_version"],
)

# EpiGraphDB database, publicly accessible, readonly
public_graph = Neo4jDB(
    hostname=env_configs["public_epigraphdb_server"],
    bolt_port=env_configs["public_epigraphdb_port"],
    user=env_configs["public_epigraphdb_user"],
    password=env_configs["public_epigraphdb_passwd"],
)

# PQTL database
pqtl = Neo4jDB(
    hostname=env_configs["pqtl_server"],
    bolt_port=env_configs["pqtl_port"],
    user=env_configs["pqtl_user"],
    password=env_configs["pqtl_passwd"],
    version=env_configs["pqtl_db_version"],
)

# other paired components
neural_url = env_configs["neural_url"]

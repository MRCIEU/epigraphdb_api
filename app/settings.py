"""
Control and configure global settings.
"""
from pathlib import Path

from app.utils.database import Neo4jDB
from epigraphdb_common_utils.api_env_configs import configs as api_env_configs

# General config
epigraphdb_version = "0.3"
api_version = "0.3"
api_private_access = api_env_configs["api_private_access"]
if api_private_access:
    api_version = f"{api_version}-private"

api_key = api_env_configs["api_key"]

# directories
log_dir = Path("/tmp/epigraphdb_api/logs")
cache_dir = Path("/tmp/epigraphdb_api/cache")
log_dir.mkdir(parents=True, exist_ok=True)
cache_dir.mkdir(parents=True, exist_ok=True)

# EpiGraphDB database
epigraphdb = Neo4jDB(
    hostname=api_env_configs["epigraphdb_server"],
    bolt_port=api_env_configs["epigraphdb_port"],
    user=api_env_configs["epigraphdb_user"],
    password=api_env_configs["epigraphdb_passwd"],
    version=api_env_configs["epigraphdb_db_version"],
)

# PQTL database
pqtl = Neo4jDB(
    hostname=api_env_configs["pqtl_server"],
    bolt_port=api_env_configs["pqtl_port"],
    user=api_env_configs["pqtl_user"],
    password=api_env_configs["pqtl_passwd"],
    version=api_env_configs["pqtl_db_version"],
)

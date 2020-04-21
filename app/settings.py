"""
Control and configure global settings.
"""
from pathlib import Path

from environs import Env
from loguru import logger

from app.utils.database import Neo4jDB

# Loads environmental variables from .env
env = Env()
env.read_env()

# General config
epigraphdb_version = "0.2"
api_version = "0.3"
api_private_access = env.bool("API_PRIVATE_ACCESS", False)
if api_private_access:
    api_version = f"{api_version}-private"

# API config
debug = env.bool("DEBUG", True)
api_port = env.int("API_PORT", 8005)
# api_key: for public endpoints with restricted access
api_key = env.str("API_KEY", None)
if api_key is None:
    logger.warning("api_key is None")

# directories
log_dir = Path("/tmp/epigraphdb_api/logs")
cache_dir = Path("/tmp/epigraphdb_api/cache")
log_dir.mkdir(parents=True, exist_ok=True)
cache_dir.mkdir(parents=True, exist_ok=True)

# EpiGraphDB database
epigraphdb = Neo4jDB(
    hostname=env.str("EPIGRAPHDB_SERVER", "0.0.0.0"),
    bolt_port=env.str("EPIGRAPHDB_PORT", "7687"),
    user=env.str("EPIGRAPHDB_USER", "neo4j"),
    password=env.str("EPIGRAPHDB_PASSWD", "neo4j"),
    version=env.str("EPIGRAPHDB_DB_VERSION", ""),
)
epigraphdb_browser = env.str("EPIGRAPHDB_DB_BROWSER", "")

# pQTL database
pqtl = Neo4jDB(
    hostname=env.str("PQTL_SERVER", ""),
    bolt_port=env.str("PQTL_PORT", ""),
    user=env.str("PQTL_USER", "neo4j"),
    password=env.str("PQTL_PASSWD", "neo4j"),
    version=env.str("PQTL_DB_VERSION", ""),
)

env_configs = {
    "api_private_access": api_private_access,
    "api_key[:5]": str(api_key)[:5],
    "api_port": api_port,
    "epigraphdb": {
        "hostname": epigraphdb.hostname,
        "bolt_port": epigraphdb.bolt_port,
        "version": epigraphdb.version,
        "epigraphdb_browser": epigraphdb_browser,
    },
    "pqtl": {
        "hostname": pqtl.hostname,
        "bolt_port": pqtl.bolt_port,
        "version": pqtl.version,
    },
}

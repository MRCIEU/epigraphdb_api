import re
from typing import Any, Dict, Optional

from loguru import logger


def format_response(
    data: Any,
    query: Optional[str] = None,
    total_seconds: Optional[float] = None,
    logging: bool = True,
) -> Dict:
    """Format response from cypher query into
    {
        "metadata": [...]
        "query": query
    }
    """
    if query is not None:
        query = trim_cypher_query(query)
    if logging:
        logger.info(f"query: {query}")
    results = data
    empty_results = True
    if len(results) > 0:
        empty_results = False
    metadata = {
        "query": query,
        "total_seconds": total_seconds,
        "empty_results": empty_results,
    }
    out = {"metadata": metadata, "results": results}
    return out


def trim_cypher_query(query: str) -> str:
    """Remove redundant whitespaces from a cypher query."""
    formatted_query = re.sub(r"\s+", " ", query).strip()
    return formatted_query

from dataclasses import dataclass
from datetime import datetime
from time import sleep
from typing import Optional

from fastapi import HTTPException
from loguru import logger
from neo4j import GraphDatabase
from neobolt.exceptions import (
    CypherError,
    CypherSyntaxError,
    CypherTypeError,
    ServiceUnavailable,
)

from app.utils.process_query import format_response

DRIVER_KWARGS = {
    "encrypted": False,
    # "keep_alive": False,
}
MAX_TRY = 4
RETRY_SEC = 2


@dataclass
class Neo4jDB:
    """A dataclass for neo4j database."""

    hostname: str
    bolt_port: str
    user: Optional[str] = None
    password: Optional[str] = None
    version: Optional[str] = None

    def __post_init__(self):
        if self.version is None:
            self.version = ""
        self._driver = None

    def run_query(self, query, format=True):
        """Run query to Neo4jDB, if format then
        post process using `format_response`
        """
        start_time = datetime.now()
        for try_idx in range(MAX_TRY):
            try:
                if self.user is not None:
                    driver = GraphDatabase.driver(
                        f"bolt://{self.hostname}:{self.bolt_port}",
                        auth=(self.user, self.password),
                        **DRIVER_KWARGS,
                    )
                else:
                    driver = GraphDatabase.driver(
                        f"bolt://{self.hostname}:{self.bolt_port}",
                        **DRIVER_KWARGS,
                    )
                with driver.session() as session:
                    data = session.run(query).data()
                driver.close()
            except ServiceUnavailable as e:
                if try_idx < MAX_TRY - 1:
                    logger.exception(
                        f"ServiceUnavailable: {e}; "
                        + f"retry after {RETRY_SEC} seconds; "
                        + f"current retry #{try_idx}"
                    )
                    sleep(RETRY_SEC)
                    continue
                else:
                    raise
            except CypherSyntaxError as e:
                raise HTTPException(
                    status_code=422, detail=f"CypherSyntaxError: {e}"
                )
            except CypherTypeError as e:
                raise HTTPException(
                    status_code=422, detail=f"CypherTypeError: {e}"
                )
            except CypherError as e:
                raise HTTPException(
                    status_code=422, detail=f"CypherError: {e}"
                )
            break
        finish_time = datetime.now()
        total_seconds = (finish_time - start_time).total_seconds()
        if format:
            return format_response(data, query, total_seconds=total_seconds)
        else:
            return data

    def check_connection(self) -> bool:
        try:
            self.run_query("MATCH (n) RETURN n LIMIT 0;")
        except Exception:
            return False
        return True

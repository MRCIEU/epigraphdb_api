from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from neo4j import GraphDatabase
from neobolt.exceptions import CypherError, CypherSyntaxError, CypherTypeError

from app.utils.process_query import format_response


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

    def close(self):
        self._driver.close()

    def run_query(self, query, format=True):
        """Run query to Neo4jDB, if format then
        post process using `format_respose`
        """
        if self.user is not None:
            self._driver = GraphDatabase.driver(
                f"bolt://{self.hostname}:{self.bolt_port}",
                auth=(self.user, self.password),
                max_connection_lifetime=20,
            )
        else:
            self._driver = GraphDatabase.driver(
                f"bolt://{self.hostname}:{self.bolt_port}",
                max_connection_lifetime=20,
            )
        start_time = datetime.now()
        try:
            with self._driver.session() as session:
                data = session.run(query).data()
                session.close()
        except CypherSyntaxError as e:
            raise HTTPException(
                status_code=422, detail=f"CypherSyntaxError: {e}"
            )
        except CypherTypeError as e:
            raise HTTPException(
                status_code=422, detail=f"CypherTypeError: {e}"
            )
        except CypherError as e:
            raise HTTPException(status_code=422, detail=f"CypherError: {e}")
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

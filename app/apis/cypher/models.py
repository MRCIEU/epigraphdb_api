from pydantic import BaseModel


class CypherRequest(BaseModel):
    query: str

"""
Set up api_key logics
https://medium.com/data-rebels/fastapi-authentication-revisited-enabling-api-key-authentication-122dc5975680
"""
from typing import Union

from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader, APIKeyQuery
from starlette.status import HTTP_403_FORBIDDEN

from app.settings import api_key, api_private_access

api_key_name = "api_key"

api_key_query = APIKeyQuery(name=api_key_name, auto_error=False)
api_key_header = APIKeyHeader(name=api_key_name, auto_error=False)


def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
) -> Union[bool, str]:

    if api_private_access:
        return True
    elif api_key_query == api_key:
        return api_key_query
    elif api_key_header == api_key:
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

from typing import Dict, List

from fastapi import APIRouter

from app.resources import public_endpoints
from app.utils.logging import log_args

from .functions import process_url

router = APIRouter()


@router.get("/meta/api-endpoints", response_model=List[Dict[str, str]])
def get_meta_api_endpoints() -> List[Dict[str, str]]:
    """EXPERIMENTAL. List currently available endpoints
    for downstream uses.
    """

    def _process(endpoint_name, endpoint_info) -> Dict[str, str]:
        res = {
            "name": endpoint_name,
            "url": process_url(endpoint_name),
        }
        return res

    log_args(api="/meta/api-endpoints")
    topic_endpoints = [
        _process(key, value)
        for key, value in public_endpoints.topic_params.items()
    ]
    utility_endpoints = [
        _process(key, value)
        for key, value in public_endpoints.util_params.items()
    ]
    res = topic_endpoints + utility_endpoints
    return res

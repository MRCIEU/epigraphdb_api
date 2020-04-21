import json
from typing import Any, Callable, Dict, Optional

from app.settings import cache_dir
from app.utils.logging import logger


def cache_func_call_json(
    cache_name: str,
    func: Callable,
    params: Optional[Dict[str, Any]] = None,
    overwrite: bool = False,
):
    """Write cache to a json file.

    - cache_name: name, no extension
    """
    cache_file = cache_dir / f"{cache_name}.json"
    if overwrite or not cache_file.exists():
        if params is None:
            res = func()
        else:
            res = func(**params)
        logger.info(f"write to: {cache_file}")
        with open(cache_file, "w") as f:
            json.dump(res, f)
    else:
        logger.info(f"reuse: {cache_file}")
        with open(cache_file, "r") as f:
            res = json.load(f)
    return res

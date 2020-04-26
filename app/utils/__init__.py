from typing import List, Optional

import pandas as pd
from loguru import logger


def cypher_fuzzify(text: Optional[str]) -> Optional[str]:
    """
    Turn "{text}" to "(?i).*{text}.*"
    """
    if text is None:
        return None
    else:
        return "(?i).*{text}.*".format(text=text.lower())


def df_coerce(
    df: pd.DataFrame, list_columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """Coerce df by:

    - sort rows by values
    - If supplied, sort elems for columns that are of type list

    This is primarily for unit testing dataframes.
    """

    # Remove missing for correct inference of column types
    df = df.dropna()
    bool_number_cols = df.select_dtypes(
        include=["bool", "number"]
    ).columns.tolist()
    string_type_map = df.applymap(lambda x: isinstance(x, str)).all(0)
    string_cols = [i for i in string_type_map.index if string_type_map[i]]
    cols = list(set(bool_number_cols).union(set(string_cols)))
    logger.info(f"sort by cols: {cols}")
    if list_columns is not None:
        for col in list_columns:
            df[col] = df[col].apply(
                lambda x: sorted(x) if x is not None else x
            )
    df = df.sort_values(by=cols, kind="mergesort").reset_index(drop=True)

    return df

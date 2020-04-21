from fastapi import HTTPException


def validate_at_least_one_not_none(members):
    """
    Validate that at least one of the members is not None
    """
    if sum([value is None for key, value in members.items()]) == len(
        members.keys()
    ):
        message = (
            "At least one of the following parameters should be non-missing: "
            + "[{items}]".format(items=", ".join(members.keys()))
        )
        raise HTTPException(status_code=422, detail=message)


def validate_char_length(members, char_limit: int = 4):
    """
    Validate character length of members
    """
    for key, value in members.items():
        if value is not None and len(value) < char_limit:
            message = f"Input length for parameter `{key}` should exceed more than {char_limit}"
            raise HTTPException(status_code=422, detail=message)

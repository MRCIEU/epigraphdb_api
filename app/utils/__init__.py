from typing import Optional


def cypher_fuzzify(text: Optional[str]) -> Optional[str]:
    """
    Turn "{text}" to "(?i).*{text}.*"
    """
    if text is None:
        return None
    else:
        return "(?i).*{text}.*".format(text=text.lower())

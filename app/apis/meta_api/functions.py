def process_url(input: str) -> str:
    exclude_chars = ["/", "{", "}"]
    api_doc_page = "https://docs.epigraphdb.org/api/api-endpoints/"
    anchor = input.lower().replace(" ", "-")
    for char in exclude_chars:
        anchor = anchor.replace(char, "")
    url = f"{api_doc_page}#{anchor}"
    return url

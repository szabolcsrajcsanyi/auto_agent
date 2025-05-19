from langchain.tools import tool
import urllib.request
import urllib.error
import json

@tool(parse_docstring=True)
def retrieve_openapi_spec(url: str) -> dict:
    """Retrieve and parse the OpenAPI specification from the given URL.

    Args:
        url (str): The URL of the OpenAPI JSON documentation.

    Returns:
        dict: The parsed OpenAPI specification as a Python dictionary.

    Raises:
        urllib.error.URLError: If there is an error fetching the URL.
        ValueError: If the fetched content is not valid JSON.
    """
    try:
        with urllib.request.urlopen(url) as response:
            charset = response.headers.get_content_charset() or 'utf-8'
            raw_data = response.read().decode(charset)
            return json.loads(raw_data)
    except urllib.error.URLError as e:
        raise urllib.error.URLError(f"Failed to fetch URL {url}: {e.reason}")
    except ValueError as e:
        raise ValueError(f"Failed to parse JSON from {url}: {str(e)}")
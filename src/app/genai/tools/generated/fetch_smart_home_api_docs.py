from typing import Any, Dict
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import json
from langchain.tools import tool


@tool(parse_docstring=True)
def fetch_smart_home_api_docs(documentation_url: str) -> Dict[str, Any]:
    """Retrieve JSON documentation for a Smart Home API.

    Args:
        documentation_url (str): The HTTP or HTTPS URL pointing to the Smart Home
            API's JSON documentation.

    Returns:
        Dict[str, Any]: A dictionary representing the parsed JSON documentation.

    Raises:
        RuntimeError: If a network error occurs or the server returns a non-200
            HTTP status code.
        ValueError: If the response content cannot be parsed as valid JSON.
    """
    request = Request(
        documentation_url,
        headers={"User-Agent": "SmartHomeDocFetcher/1.0"},
        method="GET",
    )

    try:
        with urlopen(request, timeout=10) as response:
            if response.status != 200:
                raise RuntimeError(
                    f"Failed to retrieve documentation: HTTP {response.status}"
                )
            content_bytes = response.read()
    except HTTPError as exc:
        raise RuntimeError(
            f"HTTP error while retrieving documentation: {exc.reason}"
        ) from exc
    except URLError as exc:
        raise RuntimeError(
            f"Network error while retrieving documentation: {exc.reason}"
        ) from exc

    try:
        content_str = content_bytes.decode(response.headers.get_content_charset() or "utf-8")
        json_data: Dict[str, Any] = json.loads(content_str)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Received content is not valid JSON") from exc

    return json_data
from langchain.tools import tool
import urllib.request
import json

@tool(parse_docstring=True)
def access_smart_home_api(url: str) -> dict:
    """Access the smart home API documentation.

    Args:
        url (str): The URL of the smart home API documentation.

    Returns:
        dict: The parsed JSON content of the API documentation.
    """
    with urllib.request.urlopen(url) as response:
        data = response.read()
        return json.loads(data)
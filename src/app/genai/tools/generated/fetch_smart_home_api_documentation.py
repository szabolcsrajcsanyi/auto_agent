from langchain.tools import tool
import requests

@tool(parse_docstring=True)
def fetch_smart_home_api_documentation(api_url: str) -> dict:
    """Fetch the smart home API documentation from the given URL.

    Args:
        api_url (str): The URL of the smart home API documentation.

    Returns:
        dict: The parsed JSON content of the API documentation.
    """
    response = requests.get(api_url)
    response.raise_for_status()
    return response.json()
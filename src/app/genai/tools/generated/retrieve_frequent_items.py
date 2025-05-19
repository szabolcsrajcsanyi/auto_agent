from langchain.tools import tool
import urllib.request
import urllib.error
import json

@tool(parse_docstring=True)
def retrieve_frequent_items(base_url: str, user_id: str) -> list:
    """
    Retrieves the list of items frequently bought by a user from the Shopping History API.

    Args:
        base_url (str): The base URL of the Shopping History API (e.g., "http://shopping_history").
        user_id (str): The UUID of the user whose frequent items are to be retrieved.

    Returns:
        list: A list of items frequently bought by the specified user.

    Raises:
        Exception: If the HTTP request fails or the response is invalid.
    """
    endpoint = f"{base_url}/api/users/{user_id}/frequent-items"
    try:
        with urllib.request.urlopen(endpoint) as response:
            if response.status != 200:
                raise Exception(f"Failed to retrieve frequent items: HTTP {response.status}")
            payload = response.read()
        return json.loads(payload)
    except urllib.error.HTTPError as e:
        raise Exception(f"HTTP error retrieving frequent items: {e.code} {e.reason}")
    except urllib.error.URLError as e:
        raise Exception(f"URL error connecting to {endpoint}: {e.reason}")
    except json.JSONDecodeError as e:
        raise Exception(f"Error parsing JSON response: {e.msg}")
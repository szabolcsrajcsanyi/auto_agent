from langchain.tools import tool
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

@tool(parse_docstring=True)
def get_all_users(base_url: str = "http://shopping_history") -> list:
    """Retrieve a list of all users from the Shopping History API.

    Args:
        base_url (str): The base URL of the Shopping History API (e.g. "http://shopping_history").

    Returns:
        list: A list of user objects (each as a dictionary with keys like 'id' and 'name').

    Raises:
        RuntimeError: If the API request fails due to network or HTTP errors.
    """
    endpoint = f"{base_url}/api/users"
    request = Request(endpoint, headers={"Accept": "application/json"})
    try:
        with urlopen(request) as response:
            if response.status != 200:
                raise RuntimeError(f"Unexpected status code {response.status} from {endpoint}")
            data = json.load(response)
            if not isinstance(data, list):
                raise RuntimeError("API response is not a list of users.")
            return data
    except HTTPError as e:
        raise RuntimeError(f"HTTP error {e.code} when accessing {endpoint}: {e.reason}")
    except URLError as e:
        raise RuntimeError(f"Failed to reach {endpoint}: {e.reason}")

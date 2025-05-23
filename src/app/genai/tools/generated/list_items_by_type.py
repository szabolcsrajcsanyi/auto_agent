from langchain.tools import tool
import urllib.request
import urllib.error
import json
from typing import Optional, List, Dict

@tool(parse_docstring=True)
def list_items_by_type(
    base_url: str,
    types: bool = False,
    item_type: Optional[str] = None
) -> List[Dict]:
    """
    List inventory items or item types based on input flags.

    Args:
        base_url (str): Base URL of the inventory API (e.g., http://inventory_management).
        types (bool): If True, fetches item types or items of a specific type.
        item_type (str, optional): Specific item type to filter by (only applies if types=True or types=False).

    Returns:
        list[dict]: A list of items or item types.

    Behavior:
        - If types is False and no item_type is given: return all items.
        - If types is True and no item_type is given: return all item types.
        - If types is True or False and item_type is given: return items of that type.

    Raises:
        Exception: On network or HTTP errors.
    """
    base = base_url.rstrip("/")

    if types and item_type:
        endpoint = f"{base}/api/items/types/{item_type}"
    elif types and not item_type:
        endpoint = f"{base}/api/items/types"
    elif not types and item_type:
        endpoint = f"{base}/api/items/types/{item_type}"
    else:
        endpoint = f"{base}/api/items/"

    req = urllib.request.Request(endpoint, method="GET", headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req) as response:
            if response.status != 200:
                raise Exception(f"Request failed with status code {response.status}")
            data = json.loads(response.read().decode("utf-8"))
            return data
    except urllib.error.HTTPError as e:
        raise Exception(f"HTTP Error {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        raise Exception(f"URL Error: {e.reason}")
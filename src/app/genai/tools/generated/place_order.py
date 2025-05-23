from langchain.tools import tool

@tool(parse_docstring=True)
def place_order(base_url: str, item_id: str, quantity: int) -> dict:
    """
    Place an order for a given item via the Warehouse Inventory API.

    Args:
        base_url (str): The base URL of the Warehouse Inventory API (e.g., http://inventory_management).
        item_id (str): ID of the item to order.
        quantity (int): Quantity of the item to order.

    Returns:
        dict: Parsed JSON response from the API or an error message.
    """
    import json
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError, URLError
    from urllib.parse import urljoin

    # Ensure base_url ends with a slash for correct URL joining
    normalized_base = base_url.rstrip('/') + '/'
    endpoint = urljoin(normalized_base, 'api/orders/')
    payload = json.dumps({"item_id": item_id, "quantity": quantity}).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    request = Request(endpoint, data=payload, headers=headers, method="POST")

    try:
        with urlopen(request) as response:
            body = response.read().decode("utf-8")
            return json.loads(body)
    except HTTPError as e:
        return {"error": f"HTTPError: {e.code} - {e.reason}"}
    except URLError as e:
        return {"error": f"URLError: {e.reason}"}
import requests
from langchain.tools import tool

WAREHOUSE_API_BASE_URL = "http://inventory_management/api"

@tool
def get_items_by_type(type_name: str, name_contains: str = None, max_stock: int = None) -> list:
    """
    Get all items of a given type, with optional filters by name and stock.

    Parameters:
        type_name: The type of the items to fetch (e.g. 'tool', 'storage').
        name_contains: Optional string filter to include only items containing this keyword in the name.
        max_stock: Optional filter to include only items with stock <= this value.

    Returns:
        A list of matching items with name, ID, and stock.
    """
    try:
        # Step 1: Fetch items by type
        url = f"{WAREHOUSE_API_BASE_URL}/items/types/{type_name}"
        response = requests.get(url)
        response.raise_for_status()
        items = response.json()

        if not isinstance(items, list) or not items:
            return [f"No items found for type '{type_name}'"]

        filtered_items = []

        # Step 2: Apply filters
        for item in items:
            name = item.get("name", "")
            stock = item.get("stock", None)

            if name_contains and name_contains.lower() not in name.lower():
                continue
            if max_stock is not None and (stock is None or stock > max_stock):
                continue

            filtered_items.append({
                "id": item.get("id"),
                "name": name,
                "stock": stock
            })

        if not filtered_items:
            return [f"No items matched filters in type '{type_name}'"]

        return filtered_items

    except requests.exceptions.RequestException as e:
        return [f"❌ Failed to retrieve items by type: {str(e)}"]

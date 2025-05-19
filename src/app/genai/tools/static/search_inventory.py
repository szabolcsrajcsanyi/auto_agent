import requests
from langchain.tools import tool

WAREHOUSE_API_BASE_URL = "http://inventory_management/api"
LOW_STOCK_THRESHOLD = 50  # Customize this as needed

@tool
def search_inventory(
    type_filter: str = None,
    name_contains: str = None,
    only_low_stock: bool = False
) -> list:
    """
    Search the warehouse inventory by type, partial name, or low-stock flag.

    Parameters:
        type_filter: Optional item type to filter (e.g., 'electronics').
        name_contains: Optional partial name (e.g., 'battery').
        only_low_stock: If True, only return items with low stock (below threshold).

    Returns:
        A list of items matching the criteria with id, name, stock, and type.
    """
    try:
        # Step 1: Get all items or by type
        if type_filter:
            response = requests.get(f"{WAREHOUSE_API_BASE_URL}/items/types/{type_filter}")
        else:
            response = requests.get(f"{WAREHOUSE_API_BASE_URL}/items/")
        response.raise_for_status()
        items = response.json()

        results = []

        for item in items:
            name = item.get("name", "")
            stock = item.get("stock", None)
            type_ = item.get("type", "unknown")

            # Apply optional filters
            if name_contains and name_contains.lower() not in name.lower():
                continue
            if only_low_stock and (stock is None or stock >= LOW_STOCK_THRESHOLD):
                continue

            results.append({
                "id": item.get("id"),
                "name": name,
                "stock": stock,
                "type": type_
            })

        if not results:
            return ["No items matched the provided filters."]
        return results

    except requests.exceptions.RequestException as e:
        return [f"❌ Failed to search inventory: {str(e)}"]

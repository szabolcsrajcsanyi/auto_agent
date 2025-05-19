import requests
from datetime import datetime, timedelta
from langchain.tools import tool

WAREHOUSE_API_BASE_URL = "http://inventory_management/api"

@tool
def detect_inactive_items(
    inactive_days: int = 30,
    type_filter: str = None,
    max_stock: int = None
) -> list:
    """
    Detect items that haven't been used or ordered recently.

    Parameters:
        inactive_days: Minimum number of days since the item was last ordered/used.
        type_filter: Optional item type to filter (e.g., 'tool', 'storage').
        max_stock: Optional maximum stock threshold (e.g., only show items that are also in stock).

    Returns:
        A list of inactive items with name, stock, and last activity date.
    """
    try:
        # Step 1: Fetch items (by type if specified)
        url = f"{WAREHOUSE_API_BASE_URL}/items/types/{type_filter}" if type_filter else f"{WAREHOUSE_API_BASE_URL}/items/"
        response = requests.get(url)
        response.raise_for_status()
        items = response.json()

        if not isinstance(items, list) or not items:
            return ["No items found."]

        threshold_date = datetime.now() - timedelta(days=inactive_days)
        result = []

        for item in items:
            last_used_str = item.get("last_used") or item.get("last_ordered")
            if not last_used_str:
                continue  # Skip items without activity tracking

            try:
                last_used_date = datetime.fromisoformat(last_used_str)
            except ValueError:
                continue  # Skip invalid dates

            if last_used_date > threshold_date:
                continue  # Item was used recently

            stock = item.get("stock", None)
            if max_stock is not None and (stock is None or stock > max_stock):
                continue

            result.append({
                "id": item.get("id"),
                "name": item.get("name", "Unnamed"),
                "stock": stock,
                "last_used": last_used_str,
                "type": item.get("type", "unknown")
            })

        if not result:
            return ["No inactive items matched the criteria."]
        return result

    except requests.exceptions.RequestException as e:
        return [f"❌ Failed to fetch or filter items: {str(e)}"]

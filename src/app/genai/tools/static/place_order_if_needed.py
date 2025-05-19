import requests
from langchain.tools import tool


WAREHOUSE_API_BASE_URL = "http://inventory_management/api"


@tool
def place_order_if_needed(item_id: str, quantity: int, threshold: int = 100) -> str:
    """
    Place an order for a given item if its stock is below a defined threshold.

    Parameters:
        item_id: The ID of the item to check and potentially order.
        quantity: Quantity to order if stock is too low.
        threshold: Minimum acceptable stock before triggering an order.

    Returns:
        A message indicating whether an order was placed or not.
    """
    try:
        # Step 1: Get item details (optional for better response message)
        item_resp = requests.get(f"{WAREHOUSE_API_BASE_URL}/items/{item_id}")
        item_resp.raise_for_status()
        item_data = item_resp.json()
        item_name = item_data.get("name", "Unknown Item")

        # Step 2: Check stock level
        stock_resp = requests.get(f"{WAREHOUSE_API_BASE_URL}/items/{item_id}/stock")
        stock_resp.raise_for_status()
        stock_data = stock_resp.json()
        current_stock = stock_data.get("stock")

        if current_stock is None:
            return f"❌ Failed to retrieve stock level for item '{item_name}' (ID: {item_id})."

        # Step 3: Compare with threshold
        if current_stock < threshold:
            # Step 4: Place order
            order_payload = {
                "item_id": item_id,
                "quantity": quantity
            }
            order_resp = requests.post(f"{WAREHOUSE_API_BASE_URL}/orders/", json=order_payload)
            order_resp.raise_for_status()
            return (
                f"📦 Stock for '{item_name}' is low ({current_stock} units). "
                f"An order for {quantity} more units has been placed."
            )
        else:
            return f"✅ '{item_name}' has sufficient stock: {current_stock} units. No order placed."

    except requests.exceptions.RequestException as e:
        return f"❌ Failed to process order check: {str(e)}"

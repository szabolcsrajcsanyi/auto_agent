import requests
from collections import defaultdict
from langchain.tools import tool


WAREHOUSE_API_BASE_URL = "http://inventory_management/api"
LOW_STOCK_THRESHOLD = 50


@tool
def summarize_inventory_distribution(
    include_counts: bool = True,
    include_average_stock: bool = True,
    only_low_stock: bool = False
) -> str:
    """
    Summarize how inventory is distributed across item types.

    Parameters:
        include_counts: Whether to include item counts per type.
        include_average_stock: Whether to show average stock per type.
        only_low_stock: If True, summarize only items below the low-stock threshold.

    Returns:
        A summary string describing inventory distribution.
    """
    try:
        # Step 1: Fetch all items
        response = requests.get(f"{WAREHOUSE_API_BASE_URL}/items/")
        response.raise_for_status()
        items = response.json()

        if not isinstance(items, list) or not items:
            return "No inventory data available."

        # Step 2: Group and summarize by type
        summary = defaultdict(list)

        for item in items:
            stock = item.get("stock")
            type_ = item.get("type", "Unknown")

            if stock is None:
                continue
            if only_low_stock and stock >= LOW_STOCK_THRESHOLD:
                continue

            summary[type_].append(stock)

        if not summary:
            return "No items matched the criteria."

        # Step 3: Format results
        output = ["📊 Inventory Distribution Summary:"]
        for item_type, stocks in summary.items():
            line = f"• {item_type.capitalize()}:"
            if include_counts:
                line += f" {len(stocks)} item(s)"
            if include_average_stock:
                avg = sum(stocks) / len(stocks) if stocks else 0
                line += f", avg stock: {avg:.1f}"
            output.append(line)

        return "\n".join(output)

    except requests.exceptions.RequestException as e:
        return f"❌ Failed to retrieve inventory data: {str(e)}"

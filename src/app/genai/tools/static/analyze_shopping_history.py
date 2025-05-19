import requests
from langchain.tools import tool
from datetime import datetime


SHOPPING_API_BASE_URL = "http://shopping_history/api"


@tool
def analyze_shopping_history(
    user_id: str,
    start_date: str = None,     # Format: YYYY-MM-DD
    end_date: str = None,       # Format: YYYY-MM-DD
    filter_item: str = None,
    include_total: bool = True,
    include_frequent: bool = False,
    include_recent: bool = False
) -> str:
    """
    Analyze a user's shopping history with optional filters and return selected insights.

    Parameters:
        user_id: UUID of the user.
        start_date: Optional filter to include purchases from this date.
        end_date: Optional filter to include purchases up to this date.
        filter_item: Optional keyword to include only items that match.
        include_total: Whether to include the total amount spent.
        include_frequent: Whether to include a list of most frequent items.
        include_recent: Whether to include the most recent purchase.

    Returns:
        A summary string based on selected options.
    """
    try:
        resp = requests.get(f"{SHOPPING_API_BASE_URL}/users/{user_id}/history")
        resp.raise_for_status()
        history = resp.json()

        if not history:
            return "No purchases found for this user."

        # Step 1: Filter by date and item keyword
        def filter_entry(entry):
            if start_date and entry["date"] < start_date:
                return False
            if end_date and entry["date"] > end_date:
                return False
            if filter_item and filter_item.lower() not in entry["name"].lower():
                return False
            return True

        filtered = [entry for entry in history if filter_entry(entry)]
        if not filtered:
            return "No purchases matched the given filters."

        # Step 2: Build response
        summary = []

        if include_total:
            total_spent = sum(entry["price"] * entry["quantity"] for entry in filtered)
            summary.append(f"💰 Total spent: ${total_spent:.2f}")

        if include_frequent:
            from collections import Counter
            counter = Counter(entry["name"] for entry in filtered)
            top = counter.most_common(3)
            summary.append("🔁 Frequent items: " + ", ".join(f"{item} ({count}x)" for item, count in top))

        if include_recent:
            latest = max(filtered, key=lambda e: e["date"])
            summary.append(f"🕓 Most recent: {latest['name']} on {latest['date']}")

        return "\n".join(summary)

    except requests.exceptions.RequestException as e:
        return f"❌ Failed to analyze shopping history: {str(e)}"

import requests
from langchain.tools import tool

@tool
def get_purchased_items(
    base_url: str,
    user_id: str,
    start_date: str = None,
    end_date: str = None
) -> list:
    """
    Retrieve all purchased items for a user, optionally filtered by date range.

    Parameters:
        base_url: Base URL of the Shopping History API (e.g., http://shopping_history).
        user_id: UUID of the user.
        start_date: Optional. Start date filter in 'YYYY-MM-DD' format.
        end_date: Optional. End date filter in 'YYYY-MM-DD' format.

    Returns:
        A list of purchased item names within the specified time range.
    """
    try:
        response = requests.get(f"{base_url}/api/users/{user_id}/history")
        response.raise_for_status()
        history = response.json()

        if not isinstance(history, list):
            return ["❌ Unexpected response format."]

        # Apply optional date filters
        def within_range(entry):
            date = entry.get("date")
            if start_date and date < start_date:
                return False
            if end_date and date > end_date:
                return False
            return True

        filtered = [entry["name"] for entry in history if within_range(entry)]
        return filtered

    except requests.exceptions.RequestException as e:
        return [f"❌ Request failed: {str(e)}"]

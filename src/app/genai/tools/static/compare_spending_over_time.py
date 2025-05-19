import requests
from langchain.tools import tool


SHOPPING_API_BASE_URL = "http://shopping_history/api"


@tool
def compare_spending_over_time(
    user_id: str,
    granularity: str = "month",  # "month" or "year"
    window: int = 2,              # number of periods to compare (e.g. 2 months, 2 years)
) -> str:
    """
    Compare the user's spending over the last N months or years.

    Parameters:
        user_id: UUID of the user.
        granularity: "month" or "year" for how to group the spending.
        window: How many periods (months/years) to include, must be ≥ 2.

    Returns:
        A comparison summary across time periods.
    """
    try:
        if granularity == "month":
            resp = requests.get(f"{SHOPPING_API_BASE_URL}/users/{user_id}/monthly-summary")
        elif granularity == "year":
            resp = requests.get(f"{SHOPPING_API_BASE_URL}/users/{user_id}/yearly-summary")
        else:
            return "Invalid granularity: must be 'month' or 'year'."

        resp.raise_for_status()
        data = resp.json()

        if not isinstance(data, dict) or len(data) < window:
            return f"Not enough {granularity}ly data to compare the last {window} periods."

        # Sort by date descending (e.g., most recent month/year first)
        sorted_periods = sorted(data.keys(), reverse=True)[:window]

        # Build comparison output
        lines = []
        for period in sorted_periods:
            entries = data[period]
            if isinstance(entries, list):
                total = sum(item["price"] * item["quantity"] for item in entries)
            else:
                total = sum(e.get("price", 0) * e.get("quantity", 1) for e in entries)
            lines.append((period, total))

        summary = "\n".join([f"{period}: ${amount:.2f}" for period, amount in lines])
        trend = "📈 Increasing" if lines[0][1] > lines[1][1] else "📉 Decreasing" if lines[0][1] < lines[1][1] else "➡️ Same spending"

        return f"Spending comparison over the last {window} {granularity}s:\n{summary}\nTrend: {trend}"

    except requests.exceptions.RequestException as e:
        return f"❌ Failed to fetch comparison data: {str(e)}"

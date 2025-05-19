from langchain.tools import tool
import urllib.request
import urllib.error
import json

@tool(parse_docstring=True)
def get_monthly_summary(user_id: str, base_url: str = "http://shopping_history") -> dict:
    """Retrieve the monthly summary of purchases for a specific user.

    Args:
        user_id (str): UUID of the user (e.g., Charlie's user_id).
        base_url (str): Base URL of the Shopping History API.

    Returns:
        dict: Parsed JSON response containing monthly purchase summaries.
    """
    url = f"{base_url}/api/users/{user_id}/monthly-summary"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req) as resp:
            if resp.status != 200:
                raise urllib.error.HTTPError(url, resp.status, resp.reason, resp.headers, None)
            data = json.load(resp)
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP Error {e.code}: {e.reason}"}
    except urllib.error.URLError as e:
        return {"error": f"URL Error: {e.reason}"}
    return data
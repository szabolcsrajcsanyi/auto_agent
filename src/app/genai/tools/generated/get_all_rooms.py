from langchain.tools import tool
import urllib.request
import urllib.error
import json
from typing import List, Dict, Optional, Union

@tool(parse_docstring=True)
def get_all_rooms(
    api_base_url: str,
    room_id: Optional[str] = None,
    filter_name: Optional[str] = None
) -> Union[Dict, List[Dict]]:
    """
    Query the smart home API to retrieve one or more rooms.

    Args:
        api_base_url (str): The base URL of the smart home API (e.g., "http://smart_home").
        room_id (Optional[str]): If provided, fetch only the room with this ID.
        filter_name (Optional[str]): If provided, return only rooms whose name includes this string (case-insensitive).

    Returns:
        Union[Dict, List[Dict]]: A single room dict if room_id is provided, or a list of rooms (optionally filtered by name).
    """
    try:
        if room_id:
            url = f"{api_base_url.rstrip('/')}/api/rooms/{room_id}"
            request = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(request) as response:
                body = response.read().decode("utf-8")
                return json.loads(body)
        else:
            url = f"{api_base_url.rstrip('/')}/api/rooms/"
            request = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(request) as response:
                body = response.read().decode("utf-8")
                rooms = json.loads(body)

            if filter_name:
                filter_lower = filter_name.lower()
                rooms = [r for r in rooms if filter_lower in r.get("name", "").lower()]

            return rooms

    except urllib.error.HTTPError as e:
        return {"error": f"HTTP error {e.code}: {e.reason}"}
    except urllib.error.URLError as e:
        return {"error": f"URL error: {e.reason}"}

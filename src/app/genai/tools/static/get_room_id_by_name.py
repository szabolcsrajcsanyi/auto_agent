import requests
import json
from langchain.tools import tool


@tool(parse_docstring=True)
def get_room_id_by_name(base_url: str, room_name: str = "Kitchen") -> str:
    """Fetch the ID of a specific room by name from the smart home API.

    Args:
        base_url (str): The base URL of the smart home API.
        room_name (str, optional): The name of the room to search for. Defaults to "Kitchen".

    Returns:
        str: The room ID as a string, or a JSON error message string if not found or on error.
    """
    try:
        url = f"{base_url}/api/rooms/"
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        rooms = response.json()

        for room in rooms:
            if room.get("name", "").lower() == room_name.lower():
                return room.get("id", "")

        return json.dumps({"error": f"Room '{room_name}' not found."})
    except requests.exceptions.RequestException as e:
        return json.dumps({"error": f"Request failed: {str(e)}"})
    except (ValueError, TypeError) as e:
        return json.dumps({"error": f"Invalid JSON response: {str(e)}"})
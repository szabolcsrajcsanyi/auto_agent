import requests
from langchain.tools import tool


SMART_HOME_BASE_URL = "http://smart_home/api"


@tool
def get_room_details(
    room_name: str,
    include_devices: bool = True,
    full_device_info: bool = True,
    filter_device_type: str = None
) -> dict:
    """
    Get details about a room by name, including optional device info.

    Parameters:
        room_name: The name of the room (case-insensitive).
        include_devices: Whether to include devices at all.
        full_device_info: If True, return full device info. If False, return name and type only.
        filter_device_type: Optionally return only devices of a specific type (e.g., 'light', 'thermostat').

    Returns:
        A dictionary with room metadata and optionally filtered/summarized devices.
    """
    try:
        # Step 1: Fetch all rooms
        rooms_resp = requests.get(f"{SMART_HOME_BASE_URL}/rooms/")
        rooms_resp.raise_for_status()
        rooms = rooms_resp.json()

        # Step 2: Find the matching room
        matching_room = next((r for r in rooms if r["name"].lower() == room_name.lower()), None)
        if not matching_room:
            return {"error": f"No room found with name '{room_name}'."}

        room_id = matching_room["id"]

        # Step 3: Get room metadata
        room_detail_resp = requests.get(f"{SMART_HOME_BASE_URL}/rooms/{room_id}")
        room_detail_resp.raise_for_status()
        room_detail = room_detail_resp.json()

        # Step 4: Optionally fetch device details
        if not include_devices:
            return {
                "id": room_detail["id"],
                "name": room_detail["name"],
                "description": room_detail["description"]
            }

        detailed_devices = []
        for device_id in room_detail.get("devices", []):
            device_resp = requests.get(f"{SMART_HOME_BASE_URL}/devices/{device_id}")
            if device_resp.status_code != 200:
                continue

            device = device_resp.json()
            if filter_device_type and device.get("type") != filter_device_type:
                continue

            if full_device_info:
                detailed_devices.append(device)
            else:
                detailed_devices.append({
                    "id": device["id"],
                    "name": device["name"],
                    "type": device["type"]
                })

        return {
            "id": room_detail["id"],
            "name": room_detail["name"],
            "description": room_detail["description"],
            "devices": detailed_devices
        }

    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP error: {e.response.status_code} - {e.response.text}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

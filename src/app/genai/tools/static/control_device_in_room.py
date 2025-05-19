import requests
from langchain.tools import tool


SMART_HOME_BASE_URL = "http://smart_home/api"


@tool
def control_device_in_room(room_name: str, device_type: str, command: dict) -> dict:
    """
    Control a device of a given type in a specific room using a command.

    Parameters:
        room_name: Partial or full name of the room (e.g. 'kitchen', 'living').
        device_type: Type of the device ('light', 'thermostat', 'lock', 'speaker', 'camera', 'blinds').
        command: Dictionary of settings to send to the device (depends on device type).

    Returns:
        The updated device state or an error message.
    """
    try:
        # Step 1: Get all rooms
        rooms_resp = requests.get(f"{SMART_HOME_BASE_URL}/rooms/")
        rooms_resp.raise_for_status()
        rooms = rooms_resp.json()

        # Step 2: Fuzzy match room name
        matching_room = next(
            (r for r in rooms if room_name.lower() in r["name"].lower()),
            None
        )
        if not matching_room:
            return {"error": f"No room found matching '{room_name}'."}

        room_id = matching_room["id"]

        # Step 3: Get all devices in the room
        devices_resp = requests.get(f"{SMART_HOME_BASE_URL}/rooms/{room_id}/devices")
        devices_resp.raise_for_status()
        devices = devices_resp.json()

        # Step 4: Find first matching device of the given type
        target_device = next((d for d in devices if d["type"] == device_type), None)
        if not target_device:
            return {"error": f"No device of type '{device_type}' found in room '{matching_room['name']}'."}

        device_id = target_device["id"]

        # Step 5: Send command
        patch_resp = requests.patch(
            f"{SMART_HOME_BASE_URL}/devices/{device_id}/command",
            json=command
        )
        patch_resp.raise_for_status()
        return patch_resp.json()

    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

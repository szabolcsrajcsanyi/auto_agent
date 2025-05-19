from typing import List, Optional
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from langchain.tools import tool

@tool(parse_docstring=True)
def get_device_ids_in_room(api_base_url: str, room_id: str, device_type: Optional[str] = None) -> List[str]:
    """
    Retrieves the device IDs of all devices in a specific room, optionally filtered by device type.

    Args:
        api_base_url (str): Base URL of the Smart Home API (e.g., 'http://smart_home').
        room_id (str): UUID of the room whose devices should be retrieved.
        device_type (Optional[str]): Type of device to filter (e.g., 'light', 'speaker', 'thermostat').
                                     If not specified, returns all device IDs in the room.

    Returns:
        List[str]: A list of device IDs for matching devices in the specified room.

    Raises:
        RuntimeError: If the API request fails or returns a non-200 status code.
        ValueError: If the response format is unexpected.
    """
    url = f"{api_base_url.rstrip('/')}/api/rooms/{room_id}/devices"
    request = Request(url, method="GET")

    try:
        with urlopen(request) as response:
            if response.status != 200:
                raise RuntimeError(f"Unexpected status code: {response.status}")
            payload = response.read()
    except HTTPError as e:
        raise RuntimeError(f"HTTP error occurred: {e.code} {e.reason}")
    except URLError as e:
        raise RuntimeError(f"URL error occurred: {e.reason}")

    try:
        data = json.loads(payload)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Invalid JSON response: {e.msg}")

    if isinstance(data, dict) and "devices" in data:
        devices = data["devices"]
    elif isinstance(data, list):
        devices = data
    else:
        raise ValueError("Unexpected response format: expected a list or dict with 'devices' key")

    filtered_devices = [
        device["id"]
        for device in devices
        if "id" in device and (device_type is None or device.get("type") == device_type)
    ]
    return filtered_devices

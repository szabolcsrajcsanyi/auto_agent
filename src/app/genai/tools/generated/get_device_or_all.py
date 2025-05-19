import requests
from langchain.tools import tool
from typing import Optional, Union, List

@tool
def get_device_or_all(
    base_url: str,
    device_id: Optional[str] = None,
    filter_type: Optional[str] = None
) -> Union[dict, List[dict]]:
    """
    Retrieve a specific device by ID or all devices if no ID is given.
    Optionally filter by device type.

    Parameters:
        base_url: The base URL of the smart home API (e.g. 'http://smart_home/api').
        device_id: Optional UUID of the device to retrieve.
        filter_type: Optional device type to filter results (e.g., 'light', 'thermostat').

    Returns:
        A single device dict if device_id is provided, or a list of devices if not.
        If filter_type is provided, only matching types are returned.
    """
    try:
        if device_id:
            # Fetch a specific device
            resp = requests.get(f"{base_url}/devices/{device_id}")
            resp.raise_for_status()
            device = resp.json()
            if filter_type and device.get("type") != filter_type:
                return {"id": device_id, "error": f"Device type does not match filter '{filter_type}'."}
            return device
        else:
            # Fetch all devices
            resp = requests.get(f"{base_url}/devices/")
            resp.raise_for_status()
            devices = resp.json()
            if filter_type:
                devices = [d for d in devices if d.get("type") == filter_type]
            return devices

    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

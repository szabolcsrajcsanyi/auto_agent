import requests
from langchain.tools import tool

SMART_HOME_BASE_URL = "http://smart_home/api"


@tool
def get_device_info(device_id: str = None, device_name: str = None) -> dict:
    """
    Get the current status and settings of a smart home device.

    You can either provide a device_id (UUID) or a partial device_name to look it up.

    Parameters:
        device_id: UUID of the device (optional if device_name is used).
        device_name: Partial name of the device (case-insensitive match).

    Returns:
        The device metadata and current settings, or an error message.
    """
    try:
        if not device_id and not device_name:
            return {"error": "You must provide either device_id or device_name."}

        # Resolve device by name if only name is given
        if not device_id and device_name:
            # Step 1: Get all devices
            devices_resp = requests.get(f"{SMART_HOME_BASE_URL}/devices/")
            devices_resp.raise_for_status()
            devices = devices_resp.json()

            # Step 2: Find device by partial name match (case-insensitive)
            matching_device = next(
                (d for d in devices if device_name.lower() in d["name"].lower()),
                None
            )
            if not matching_device:
                return {"error": f"No device found matching name '{device_name}'."}
            device_id = matching_device["id"]

        # Step 3: Fetch device by ID
        device_resp = requests.get(f"{SMART_HOME_BASE_URL}/devices/{device_id}")
        device_resp.raise_for_status()
        return device_resp.json()

    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP error: {e.response.status_code} - {e.response.text}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

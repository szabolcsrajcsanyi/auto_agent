from typing import Optional, Dict, Any
from langchain.tools import tool
import urllib.request
import urllib.error
import json

@tool(parse_docstring=True)
def command_light_device(
    api_base_url: str,
    device_id: str,
    is_on: Optional[bool] = None,
    brightness: Optional[int] = None,
    color: Optional[str] = None
) -> Dict[str, Any]:
    """Send a command to a single light device using optional settings.

    Sends a PATCH request to `/api/devices/{device_id}/command` with any combination
    of the following optional light settings: is_on, brightness, and color.

    Args:
        api_base_url (str): Base URL of the smart home API (e.g., "http://smart_home").
        device_id (str): UUID of the device to control.
        is_on (Optional[bool]): Whether the light should be turned on or off.
        brightness (Optional[int]): Brightness level (0-100).
        color (Optional[str]): Desired color (e.g., "warm white", "blue").

    Returns:
        Dict[str, Any]: A dictionary with the status code and parsed response or error.
    """
    url = f"{api_base_url.rstrip('/')}/api/devices/{device_id}/command"

    # Construct payload with only non-None values
    payload_dict = {}
    if is_on is not None:
        payload_dict["is_on"] = is_on
    if brightness is not None:
        payload_dict["brightness"] = brightness
    if color is not None:
        payload_dict["color"] = color

    if not payload_dict:
        return {"error": "No settings provided. Nothing to command."}

    payload = json.dumps(payload_dict).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="PATCH"
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            body = response.read().decode("utf-8")
            try:
                parsed = json.loads(body)
            except json.JSONDecodeError:
                parsed = body
            return {
                "status_code": response.getcode(),
                "response": parsed
            }
    except urllib.error.HTTPError as http_err:
        return {
            "status_code": http_err.code,
            "error": http_err.reason
        }
    except urllib.error.URLError as url_err:
        return {
            "error": str(url_err.reason)
        }

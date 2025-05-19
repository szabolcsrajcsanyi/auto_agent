from typing import Optional, Dict, Any
from langchain.tools import tool
import urllib.request
import urllib.error
import json


@tool(parse_docstring=True)
def command_thermostat_device(
    api_base_url: str,
    device_id: str,
    mode: Optional[str] = None,
    target_temperature: Optional[float] = None
) -> Dict[str, Any]:
    """Send a command to a thermostat device with optional settings.

    Sends a PATCH request to `/api/devices/{device_id}/command` using any of the following:
    mode and/or target_temperature.

    Args:
        api_base_url (str): Base URL of the smart home API (e.g., "http://smart_home").
        device_id (str): UUID of the thermostat device.
        mode (Optional[str]): Desired mode, one of: "cool", "heat", "auto", "off".
        target_temperature (Optional[float]): Target temperature to set.

    Returns:
        Dict[str, Any]: A dictionary with the status code and parsed response or error.
    """
    url = f"{api_base_url.rstrip('/')}/api/devices/{device_id}/command"

    payload_dict = {}
    if mode is not None:
        payload_dict["mode"] = mode
    if target_temperature is not None:
        payload_dict["target_temperature"] = target_temperature

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

from fastapi import APIRouter, HTTPException
from uuid import UUID
from typing import List

from app.models.device import Device, DeviceSettings
from app.data import DEVICES_DB


router_devices = APIRouter(prefix="/devices")


@router_devices.get("/", response_model=List[Device], tags=["devices"])
def get_all_devices():
    return list(DEVICES_DB.values())


@router_devices.get("/{device_id}", response_model=Device, tags=["devices"])
def get_device(device_id: UUID):
    device = DEVICES_DB.get(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router_devices.patch("/{device_id}/command", response_model=Device, tags=["devices"])
def command_device(device_id: UUID, command: DeviceSettings):
    device = DEVICES_DB.get(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    # Here you would typically send the command to the actual device
    # For this example, we'll just simulate it by updating the settings
    device.settings = command
    return device

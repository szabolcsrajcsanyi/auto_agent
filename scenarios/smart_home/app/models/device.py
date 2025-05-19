from pydantic import BaseModel, Field
from typing import Optional, Literal, Union
from uuid import UUID

from app.models.device_type import (
    LightDeviceSettings,
    ThermostatDeviceSettings,
    CameraDeviceSettings,
    SpeakerDeviceSettings,
    BlindsDeviceSettings,
    LockDeviceSettings,
)


class DeviceBase(BaseModel):
    name: str
    room_id: UUID
    type: Literal["light", "thermostat", "camera", "speaker", "blinds", "lock"]
    description: Optional[str] = None


# Union type for polymorphic settings
DeviceSettings = Union[
    LightDeviceSettings,
    ThermostatDeviceSettings,
    CameraDeviceSettings,
    SpeakerDeviceSettings,
    BlindsDeviceSettings,
    LockDeviceSettings,
]


class Device(DeviceBase):
    id: UUID
    settings: DeviceSettings

    class Config:
        orm_mode = True
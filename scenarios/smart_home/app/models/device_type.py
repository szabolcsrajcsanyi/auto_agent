from pydantic import BaseModel, Field
from typing import Optional, Literal


class LightDeviceSettings(BaseModel):
    is_on: bool = False
    brightness: int = Field(0, ge=0, le=100)
    color: Optional[str] = None


class ThermostatDeviceSettings(BaseModel):
    target_temperature: float
    mode: Literal["cool", "heat", "auto", "off"]
    current_temperature: Optional[float] = None


class CameraDeviceSettings(BaseModel):
    is_recording: bool = False
    angle: Optional[int] = Field(None, ge=0, le=180)


class SpeakerDeviceSettings(BaseModel):
    volume: int = Field(50, ge=0, le=100)
    is_playing: bool = False
    current_track: Optional[str] = None


class BlindsDeviceSettings(BaseModel):
    position: int = Field(0, ge=0, le=100)  # 0=closed, 100=open


class LockDeviceSettings(BaseModel):
    is_locked: bool = True
    
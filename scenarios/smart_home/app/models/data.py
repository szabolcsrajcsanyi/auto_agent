from uuid import uuid4
from app.models.room import Room
from app.models.device import Device
from app.models.device_type import (
    LightDeviceSettings,
    ThermostatDeviceSettings,
    CameraDeviceSettings,
    SpeakerDeviceSettings,
    BlindsDeviceSettings,
    LockDeviceSettings,
)


ROOMS_DB = {}
DEVICES_DB = {}

# Create room IDs
room_names = [
    "Living Room", "Kitchen", "Master Bedroom", "Guest Bedroom",
    "Bathroom", "Garage", "Office", "Dining Room", "Hallway", "Basement"
]

room_ids = {name: uuid4() for name in room_names}

# Create devices
device_counter = 0
for room_name, room_id in room_ids.items():
    devices = []

    # Lights
    for i in range(2):
        dev_id = uuid4()
        DEVICES_DB[dev_id] = Device(
            id=dev_id,
            name=f"{room_name} Light {i+1}",
            room_id=room_id,
            type="light",
            description=f"{room_name} ceiling light {i+1}",
            settings=LightDeviceSettings(
                is_on=bool(i % 2),
                brightness=70 + i * 10,
                color="warm white" if i % 2 == 0 else "cool white"
            )
        )
        devices.append(dev_id)

    # Thermostat (only some rooms)
    if room_name in ["Living Room", "Master Bedroom", "Office"]:
        dev_id = uuid4()
        DEVICES_DB[dev_id] = Device(
            id=dev_id,
            name=f"{room_name} Thermostat",
            room_id=room_id,
            type="thermostat",
            description=f"{room_name} climate control",
            settings=ThermostatDeviceSettings(
                target_temperature=21.5,
                current_temperature=20.0 + (device_counter % 3),
                mode="auto"
            )
        )
        devices.append(dev_id)

    # Speaker
    if room_name in ["Living Room", "Dining Room", "Office"]:
        dev_id = uuid4()
        DEVICES_DB[dev_id] = Device(
            id=dev_id,
            name=f"{room_name} Speaker",
            room_id=room_id,
            type="speaker",
            description=f"Smart speaker in {room_name}",
            settings=SpeakerDeviceSettings(
                volume=50,
                is_playing=False,
                current_track=None
            )
        )
        devices.append(dev_id)

    # Camera
    if room_name in ["Garage", "Basement", "Hallway"]:
        dev_id = uuid4()
        DEVICES_DB[dev_id] = Device(
            id=dev_id,
            name=f"{room_name} Camera",
            room_id=room_id,
            type="camera",
            description=f"Security camera in {room_name}",
            settings=CameraDeviceSettings(
                is_recording=True,
                angle=90
            )
        )
        devices.append(dev_id)

    # Locks (only front facing rooms)
    if room_name in ["Garage", "Front Door", "Basement"]:
        dev_id = uuid4()
        DEVICES_DB[dev_id] = Device(
            id=dev_id,
            name=f"{room_name} Door Lock",
            room_id=room_id,
            type="lock",
            description=f"{room_name} smart lock",
            settings=LockDeviceSettings(
                is_locked=True
            )
        )
        devices.append(dev_id)

    # Blinds
    if room_name in ["Living Room", "Master Bedroom"]:
        for j in range(2):
            dev_id = uuid4()
            DEVICES_DB[dev_id] = Device(
                id=dev_id,
                name=f"{room_name} Blinds {j+1}",
                room_id=room_id,
                type="blinds",
                description=f"{room_name} blinds set {j+1}",
                settings=BlindsDeviceSettings(
                    position=50 + j * 25
                )
            )
            devices.append(dev_id)

    ROOMS_DB[room_id] = Room(
        id=room_id,
        name=room_name,
        description=f"{room_name} for simulation",
        devices=devices
    )
from fastapi import APIRouter, HTTPException
from uuid import UUID
from typing import List

from app.models.room import Room
from app.models.device import Device
from app.data import ROOMS_DB, DEVICES_DB


router_rooms = APIRouter(prefix="/rooms")


@router_rooms.get("/", response_model=List[Room], tags=["rooms"])
def get_all_rooms():
    return list(ROOMS_DB.values())


@router_rooms.get("/{room_id}", response_model=Room, tags=["rooms"])
def get_room(room_id: UUID):
    room = ROOMS_DB.get(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


@router_rooms.get("/{room_id}/devices", response_model=List[Device], tags=["rooms"])
def get_devices_in_room(room_id: UUID):
    if room_id not in ROOMS_DB:
        raise HTTPException(status_code=404, detail="Room not found")
    return [dev for dev in DEVICES_DB.values() if dev.room_id == room_id]

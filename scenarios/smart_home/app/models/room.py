from pydantic import BaseModel, Field
from uuid import UUID
from typing import List


class RoomCreate(BaseModel):
    name: str
    description: str


class Room(BaseModel):
    id: UUID
    name: str
    description: str
    devices: List[UUID] = Field(default_factory=list)

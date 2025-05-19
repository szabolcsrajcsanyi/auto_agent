from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class ItemType(str, Enum):
    TOOL = "tool"
    SAFETY = "safety"
    LIGHTING = "lighting"
    STORAGE = "storage"


class Item(BaseModel):
    id: str
    name: str
    description: str
    stock: int
    price: float
    type: ItemType

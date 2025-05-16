from pydantic import BaseModel
from datetime import datetime


class Order(BaseModel):
    id: str
    item_id: str
    quantity: int
    timestamp: datetime
    
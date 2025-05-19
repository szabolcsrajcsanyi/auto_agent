from pydantic import BaseModel
from datetime import date


class ShoppingItem(BaseModel):
    name: str
    quantity: int
    price: float
    date: date

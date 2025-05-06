from pydantic import BaseModel
from typing import List
from models.user import User
from app.models.shopping_item import ShoppingItem


class UserListResponse(BaseModel):
    users: List[User]


class ItemHistoryResponse(BaseModel):
    user_id: int
    items: List[ShoppingItem]


class FrequentItemsResponse(BaseModel):
    user_id: int
    items: List[str]


class MonthlySummary(BaseModel):
    month: str
    total_spent: float


class YearlySummary(BaseModel):
    year: int
    total_spent: float

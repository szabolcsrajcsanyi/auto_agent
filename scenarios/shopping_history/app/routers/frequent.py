from fastapi import APIRouter
from uuid import UUID
from collections import Counter
from app.data import SHOPPING_HISTORY_DB


router_frequent = APIRouter()


@router_frequent.get("/users/{user_id}/frequent-items")
def get_frequent_items(user_id: UUID):
    history = SHOPPING_HISTORY_DB.get(user_id, [])
    all_items = [item for entry in history for item in entry.items]
    counter = Counter(all_items)
    return counter.most_common(5)

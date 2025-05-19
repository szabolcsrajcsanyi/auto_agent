from fastapi import APIRouter
from uuid import UUID
from app.data import SHOPPING_HISTORY_DB


router_history = APIRouter()


@router_history.get("/users/{user_id}/history")
def get_shopping_history(user_id: UUID):
    return SHOPPING_HISTORY_DB.get(user_id, [])


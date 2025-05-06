from fastapi import APIRouter
from app.data import USERS_DB


router_users = APIRouter()


@router_users.get("/users")
def get_all_users():
    return list(USERS_DB.values())

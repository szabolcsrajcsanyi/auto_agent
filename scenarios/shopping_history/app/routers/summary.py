from fastapi import APIRouter
from uuid import UUID
from collections import defaultdict
from app.data import SHOPPING_HISTORY_DB


router_summary = APIRouter()


@router_summary.get("/users/{user_id}/monthly-summary")
def get_monthly_summary(user_id: UUID):
    history = SHOPPING_HISTORY_DB.get(user_id, [])
    summary = defaultdict(list)

    for record in history:
        month = record.date.strftime("%Y-%m")
        summary[month].append(record)

    return summary


@router_summary.get("/users/{user_id}/yearly-summary")
def get_yearly_summary(user_id: UUID):
    history = SHOPPING_HISTORY_DB.get(user_id, [])
    summary = defaultdict(list)

    for record in history:
        year = str(record.date.year)
        summary[year].append(record)

    return summary

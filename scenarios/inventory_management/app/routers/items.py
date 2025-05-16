from fastapi import APIRouter, HTTPException
from typing import List

from app.data import ITEMS_DB


router_items = APIRouter(prefix="/items", tags=["Items"])


@router_items.get("/")
def get_all_items():
    """List all items in inventory."""
    return list(ITEMS_DB.values())


@router_items.get("/types", response_model=List[str])
def get_item_types():
    """Get all available item types."""
    return list({item.type for item in ITEMS_DB.values()})


@router_items.get("/types/{type}")
def get_items_by_type(type: str):
    """Get items by type."""
    matching_items = [item for item in ITEMS_DB.values() if item.type.lower() == type.lower()]
    if not matching_items:
        raise HTTPException(status_code=404, detail=f"No items found for type: {type}")
    return matching_items


@router_items.get("/{item_id}")
def get_item(item_id: str):
    """Get item details by ID."""
    item = ITEMS_DB.get(item_id)
    if not item:
        return {"error": "Item not found"}
    return item


@router_items.get("/{item_id}/stock")
def get_item_stock(item_id: str):
    """Get stock level for a specific item."""
    item = ITEMS_DB.get(item_id)
    if item:
        return {"item_id": item_id, "stock": item.stock}
    return {"error": "Item not found"}

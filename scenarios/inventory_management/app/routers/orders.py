from fastapi import APIRouter
from uuid import uuid4
from datetime import datetime
from pydantic import BaseModel

from app.data import ORDERS_DB, ITEMS_DB
from app.models.order import Order

router_orders = APIRouter(prefix="/orders", tags=["Orders"])


class OrderRequest(BaseModel):
    item_id: str
    quantity: int


@router_orders.get("/")
def get_orders():
    """List all orders."""
    return list(ORDERS_DB.values())


@router_orders.post("/")
def create_order(order: OrderRequest):
    """Create a new order for an item."""
    item = ITEMS_DB.get(order.item_id)
    if not item:
        return {"error": "Item not found"}

    if item.stock < order.quantity:
        return {"error": "Insufficient stock"}

    item.stock -= order.quantity
    order_id = str(uuid4())
    new_order = Order(
        id=order_id,
        item_id=order.item_id,
        quantity=order.quantity,
        timestamp=datetime.utcnow()
    )
    ORDERS_DB[order_id] = new_order
    return {"status": "order placed", "order_id": order_id}
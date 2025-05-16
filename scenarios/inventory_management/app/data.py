from uuid import uuid4
from datetime import datetime, timedelta
import random

from app.models.item import Item, ItemType
from app.models.order import Order


ITEMS_DB = {}
ORDERS_DB = {}


# Items grouped by type with descriptions
typed_items = {
    ItemType.TOOL: [
        ("Cordless Drill", "High-performance 18V drill with rechargeable batteries"),
        ("Adjustable Wrench", "Heavy-duty adjustable wrench for various nut sizes"),
        ("Hammer", "16 oz claw hammer with fiberglass handle"),
        ("Socket Set", "32-piece chrome vanadium socket set with ratchet")
    ],
    ItemType.SAFETY: [
        ("Safety Gloves", "Cut-resistant gloves for industrial use"),
        ("Safety Goggles", "Anti-fog, scratch-resistant protective eyewear"),
    ],
    ItemType.LIGHTING: [
        ("LED Work Light", "Rechargeable work light with magnetic base"),
        ("Headlamp", "Adjustable LED headlamp with motion sensor")
    ],
    ItemType.STORAGE: [
        ("Storage Bin", "Stackable plastic bin with lid"),
        ("Toolbox", "Portable metal toolbox with 2 compartments")
    ]
}


# Generate items
for item_type, items in typed_items.items():
    for name, description in items:
        item_id = str(uuid4())
        ITEMS_DB[item_id] = Item(
            id=item_id,
            name=name,
            description=description,
            stock=random.randint(10, 100),
            price=round(random.uniform(10.0, 150.0), 2),
            type=item_type
        )


# Generate orders
item_ids = list(ITEMS_DB.keys())
for _ in range(15):
    item_id = random.choice(item_ids)
    quantity = random.randint(1, 10)
    order_id = str(uuid4())
    timestamp = datetime.utcnow() - timedelta(days=random.randint(0, 30))

    ORDERS_DB[order_id] = Order(
        id=order_id,
        item_id=item_id,
        quantity=quantity,
        timestamp=timestamp
    )

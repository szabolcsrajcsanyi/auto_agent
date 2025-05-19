from uuid import uuid4
from datetime import datetime, timedelta
import random

from app.models.user import User
from app.models.shopping_item import ShoppingItem


USERS_DB = {}
SHOPPING_HISTORY_DB = {}


names = ["Alice", "Bob", "Charlie", "Diana"]
item_catalog = [
    "Milk", "Bread", "Eggs", "Cheese", "Apples",
    "Bananas", "Chicken", "Beef", "Rice", "Pasta",
    "Toilet Paper", "Shampoo", "Soap", "Juice", "Cereal"
]


# Generate users
user_ids = {}
for name in names:
    uid = uuid4()
    USERS_DB[uid] = User(id=uid, name=name)
    user_ids[name] = uid


# Generate shopping history
for uid in USERS_DB:
    history = []
    current_date = datetime.now()
    for _ in range(random.randint(10, 30)):
        days_ago = random.randint(1, 180)
        date = (current_date - timedelta(days=days_ago)).date()
        for _ in range(random.randint(2, 5)):
            item = random.choice(item_catalog)
            quantity = random.randint(1, 5)
            price = round(random.uniform(1.0, 10.0), 2)
            history.append(
                ShoppingItem(
                    name=item,
                    quantity=quantity,
                    price=price,
                    date=date
                )
            )
    SHOPPING_HISTORY_DB[uid] = history

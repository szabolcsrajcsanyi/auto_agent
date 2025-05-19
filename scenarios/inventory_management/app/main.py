from fastapi import FastAPI, APIRouter

from app.routers.items import router_items
from app.routers.orders import router_orders


app = FastAPI(
    title="Warehouse Inventory API",
    version="1.0.0",
    docs_url="/api/docs", 
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)
api_router = APIRouter(prefix="/api")


api_router.include_router(router_items)
api_router.include_router(router_orders)


app.include_router(api_router)

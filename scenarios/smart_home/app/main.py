from fastapi import FastAPI, APIRouter

from app.routers.devices import router_devices
from app.routers.rooms import router_rooms



tags_metadata = [
    {
        "name": "rooms",
        "description": "Operations with rooms.",
    },
    {
        "name": "devices",
        "description": "Operations with devices.",
    },
]


app = FastAPI(
    openapi_tags=tags_metadata,
    docs_url="/api/docs", 
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)
api_router = APIRouter(prefix="/api")

api_router.include_router(router_devices)
api_router.include_router(router_rooms)

app.include_router(api_router)

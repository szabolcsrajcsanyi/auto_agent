from fastapi import FastAPI, APIRouter

from app.routers.frequent import router_frequent
from app.routers.summary import router_summary
from app.routers.history import router_history
from app.routers.users import router_users



# tags_metadata = [
#     {
#         "name": "rooms",
#         "description": "Operations with rooms.",
#     },
#     {
#         "name": "devices",
#         "description": "Operations with devices.",
#     },
# ]


app = FastAPI(
    # openapi_tags=tags_metadata,
    root_path="/api",
    docs_url="/docs", 
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)
api_router = APIRouter(prefix="/api")


api_router.include_router(router_users)
api_router.include_router(router_summary)
api_router.include_router(router_history)
api_router.include_router(router_frequent)


app.include_router(api_router)

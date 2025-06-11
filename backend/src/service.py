from fastapi import FastAPI, APIRouter

from backend.src.schema.schema import UserInput


app = FastAPI()
router = APIRouter()


@router.post("/invoke")
async def invoke(user_input: UserInput):
    pass
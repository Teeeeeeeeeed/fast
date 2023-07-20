from fastapi import APIRouter

position_router = APIRouter(tags=["Positions"], prefix="/positions")

@position_router.get("/search/{norad_id}")
async def get_position(norad_id: str):
    return {"position":norad_id}
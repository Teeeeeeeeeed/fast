from fastapi import APIRouter, Depends
from typing_extensions import Annotated
from ..services.satellite_service import search_satellite

satellite_router = APIRouter(tags=["Satellites"], prefix="/satellite")

@satellite_router.get("/search/{norad_id}")
async def search_satellites(norad_id:int, search_result: Annotated[any, Depends(search_satellite)]):
    return search_result
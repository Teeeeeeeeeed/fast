from fastapi import APIRouter, Depends
from typing_extensions import Annotated
from ..services.satellite_service import SatelliteService, search_satellite

satellite_router = APIRouter(tags=["Satellites"], prefix="/satellite")

@satellite_router.get("/search/{norad_id}")
async def search_satellites(norad_id:int, satelliteService: SatelliteService = Depends()):
    s = await satelliteService.searchByNoradID(norad_id)
    return s
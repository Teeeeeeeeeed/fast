from fastapi import APIRouter, Depends
from ..services.satellite_service import SatelliteService

satellite_router = APIRouter(tags=["Satellites"])

@satellite_router.get("/satellite/search/{search_key}")
async def search_satellites(search_key: str, satelliteService: SatelliteService = Depends()):
    print(search_key)
    return satelliteService.search_satellites(search_key)

@satellite_router.get("/satellite/search-norad/{norad_id}")
async def search_norad_satellites(norad_id:int, satelliteService: SatelliteService = Depends()):
    s = await satelliteService.searchByNoradID(norad_id)
    return s

@satellite_router.get("/satellite/get-all")
async def get_all():
    return ["all satellites"]

@satellite_router.get("/satellite/get-position-prediction/{norad_id}")
async def get_position_range(norad_id:int, satelliteService: SatelliteService = Depends()):
    return await satelliteService.get_position_range(norad_id)

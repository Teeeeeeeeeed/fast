from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from typing_extensions import Annotated
from ..services.satellite_service import SatelliteService

satellite_router = APIRouter(tags=["Satellites"], prefix="/satellite")

@satellite_router.get("/search/{search_key}")
async def search_satellites(search_key: str, satelliteService: SatelliteService = Depends()):
    return satelliteService.search_satellites(search_key)

@satellite_router.get("/search-norad/{norad_id}")
async def search_norad_satellites(norad_id:int, satelliteService: SatelliteService = Depends()):
    s = await satelliteService.searchByNoradID(norad_id)
    return s

@satellite_router.get("/get-all")
async def get_all(satelliteService: SatelliteService = Depends()):
    return satelliteService.get_all()   

@satellite_router.get("/get-position-prediction/{norad_id}")
async def get_position_range(norad_id:int, satelliteService: SatelliteService = Depends()):
    return await satelliteService.get_position_range(norad_id)

from fastapi import APIRouter, Depends
from typing_extensions import Annotated
from src.database.db import get_db_connection
from ..services.satellite_service import SatelliteService
from sqlalchemy.orm import scoped_session

satellite_router = APIRouter(tags=["Satellites"])

@satellite_router.get("/api/satellite/search/{search_key}")
async def search_satellites(search_key: str, satelliteService: SatelliteService = Depends(), db = Depends(get_db_connection)):
    return satelliteService.search_satellites(search_key, db)

@satellite_router.get("/api/satellite/search-norad/{norad_id}")
async def search_norad_satellites(norad_id:int, db = Depends(get_db_connection), satelliteService: SatelliteService = Depends()):
    return await satelliteService.searchByNoradID(norad_id, db)

@satellite_router.get("/api/satellite/get-all")
async def get_all():
    return ["all satellites"]

@satellite_router.get("/api/satellite/get-position-prediction/{norad_id}")
async def get_position_range(norad_id:int, satelliteService: SatelliteService = Depends(), db = Depends(get_db_connection)):
    return await satelliteService.get_position_range(norad_id, db)

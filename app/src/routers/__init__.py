from .satellites import satellite_router
from .positions import position_router
from fastapi import APIRouter

controllers = APIRouter()

controllers.include_router(satellite_router)
controllers.include_router(position_router)
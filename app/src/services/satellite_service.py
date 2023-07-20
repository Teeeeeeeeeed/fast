from fastapi import Depends
from app.src.database.models import Satellite

from app.src.repository.satellites_repository import SatelliteRepository
from app.src.schema.satellite import SatelliteSchema

from ..clients.noradclient import NoradClient, get_norad_client

async def search_satellite(
        norad_id:int, 
        norad_client:NoradClient = Depends(get_norad_client)):
    response = await norad_client.searchTLE(norad_id)
    return response

class SatelliteService:
    satelliteRepo: SatelliteRepository
    noradClient: NoradClient

    def __init__(self, satelliteRepository: SatelliteRepository = Depends(), noradClient: NoradClient = Depends()) -> Satellite:
        self.satelliteRepo = satelliteRepository
        self.noradClient = noradClient
    
    async def searchByNoradID(self, id:int):
        exists = await self.satelliteRepo.searchByNoradId(id)
        if (exists):
            return exists
        else:
            new_search = await self.noradClient.searchTLE(id)

            if (new_search):
                self.satelliteRepo.create(Satellite(
                    name=new_search.info.satname,
                    norad_id=new_search.info.satid,
                    tle=new_search.tle
                ))
                newSatellite = await self.satelliteRepo.searchByNoradId(new_search.info.satid)
                return newSatellite
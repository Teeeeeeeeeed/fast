import datetime
from typing import List
from fastapi import Depends
from src.database.models import Satellite

from src.repository.satellites_repository import SatelliteRepository
from src.schema.satellite import SatelliteSchema

from ..clients.noradclient import NoradClient, get_norad_client
from skyfield.api import EarthSatellite
from skyfield.api import load, wgs84

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
    
    async def searchByNoradID(self, id:int) -> List[SatelliteSchema]:
        if (not isinstance(id, int)):
            return []
        exists = self.satelliteRepo.search_by_norad_id(id)
        if (exists):
            exists = [exists]
        else:
            new_search = await self.noradClient.searchTLE(id)
            if (new_search):
                self.satelliteRepo.create(Satellite(
                    name=new_search.info.satname,
                    norad_id=new_search.info.satid,
                    tle=new_search.tle
                ))
                newSatellite = self.satelliteRepo.search_by_norad_id(new_search.info.satid)
            exists = [newSatellite]
        return list(map(self.satellite_to_metadata, exists))
    
    def search_satellites(self, key: str) -> List[SatelliteSchema]:
        s = self.satelliteRepo.search_by_name(key)
        return list(map(self.satellite_to_metadata,s))
    
    def get_all(self):
        return self.satelliteRepo.getAll()
    
    def get_position(self, s:Satellite):
        line1, line2 = s.tle.split("\r\n")
        ts = load.timescale()
        now = datetime.datetime.now()
        times = ts.utc(now.year, now.month, now.day, now.hour, now.minute, now.second)
        satellite = EarthSatellite(line1, line2)

        geocentric = satellite.at(times)

        lat, lon = wgs84.latlon_of(geocentric)
        return lat.radians,lon.radians
    
    def get_position_range(self, s: Satellite):
        line1, line2 = s.tle.split("\r\n")
        ts = load.timescale()
        now = datetime.datetime.now()
        times = ts.utc(now.year, now.month, now.day, now.hour, [ now.minute + i for i in range(-30,30,1)])
        satellite = EarthSatellite(line1, line2, "SPACE STATION")

        latitudes = []
        longitudes = []

        for time in times:
            position = satellite.at(time)
            lat, lon = wgs84.latlon_of(position)
            latitudes.append(lat.radians)
            longitudes.append(lon.radians)

        trajectory_data = [{'lat': lat, 'lon': lon} for lat, lon in zip(latitudes, longitudes)]

        return trajectory_data

    def satellite_to_metadata(self, satellite:Satellite) -> SatelliteSchema:
        map = SatelliteSchema(
            hasTle=True if len(satellite.tle) != 0 else False,
            id=satellite.id,
            name=satellite.name,
            norad_id=satellite.norad_id
        )
        return map
    
    def get_positions(self, satellites:List[int]):
        satellite_data = [self.satelliteRepo.getById(id) for id in satellites]
        satellite_position = { satellite.id: self.get_position(satellite) for satellite in satellite_data }

        return satellite_position
    
    def get_trajectories(self, satellites:List[int]):
        satellite_data = [self.satelliteRepo.getById(id) for id in satellites]
        satellite_trajectory = { satellite.id: self.get_position_range(satellite) for satellite in satellite_data }

        return satellite_trajectory

from pydantic import BaseModel

class SatelliteSchema(BaseModel):
    id: int
    norad_id: int
    satellite_name: str
    tle:str

    class Config:
        orm_mode = True
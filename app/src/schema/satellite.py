from pydantic import BaseModel

class Satellite(BaseModel):
    id: int
    norad_id: int
    satellite_name: str
    hasTle:bool

    class Config:
        orm_mode = True
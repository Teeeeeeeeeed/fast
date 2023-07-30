from typing import List
from pydantic import BaseModel

class SatelliteSchema(BaseModel):
    id: int
    name: str
    norad_id: int
    hasTle: bool

class TrajectoryRequest(BaseModel):
    ids: List[str]
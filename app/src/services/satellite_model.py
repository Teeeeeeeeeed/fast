from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database.db import Base

class Satellite(Base):
    __tablename__ = "satellite"

    id=Column(Integer, primary_key=True, index=True)
    norad_id=Column(Integer)
    satellite_name=Column(str)
    hasTle=Column(bool)
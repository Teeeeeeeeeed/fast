from typing import List, Optional
from fastapi import Depends
from app.src.database.db import get_db_connection
from app.src.database.models import Satellite
from sqlalchemy.orm import Session

class SatelliteRepository:
    __db: Session

    def __init__(self, db:Session = Depends(get_db_connection)) -> None:
        self.__db = db

    def get(self, satellite: Satellite) -> Satellite:
        return self.db.get(
            Satellite,
            satellite.id
        )
    
    def getAll(self) -> List[Satellite]:
        return self.__db.query(Satellite).all()
    
    def create(self, satellite:Satellite) -> Satellite:
        self.__db.add(satellite)
        self.__db.commit()
        self.__db.refresh(satellite)

    def update(self, id:int, satellite: Satellite) -> Satellite:
        satellite.id = id
        self.__db.merge(satellite)
        self.__db.commit()

    def delete(self, satellite: Satellite) -> None:
        self.__db.delete(satellite)
        self.__db.commit()
        self.__db.flush()
    
    def search_by_norad_id(self, norad_id: int) -> Satellite:
        return self.__db.query(Satellite).filter_by(norad_id=norad_id).first()
    
    def search_by_name(self, key: str) -> List[Satellite]:
        return self.__db.query(Satellite).filter(Satellite.name.ilike("%{0}%".format(key))).all()
    
    def getById(self, id: int) -> Satellite:
        return self.__db.query(Satellite).get(id)
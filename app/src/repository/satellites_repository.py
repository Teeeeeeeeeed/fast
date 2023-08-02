from typing import List 
from fastapi import Depends
from src.database.db import get_db_connection
from src.database.models import Satellite
from sqlalchemy.orm import Session, scoped_session

class SatelliteRepository:
    __db: Session

    def get(self, satellite: Satellite, db:Session = Depends(get_db_connection)) -> Satellite:
        return db.get(
            Satellite,
            satellite.id
        )
    
    def getAll(self, db:Session = Depends(get_db_connection)) -> List[Satellite]:
        return db.query(Satellite).all()
    
    def create(self, satellite:Satellite, db: scoped_session) -> Satellite:
        db.add(satellite)
        db.commit()
        db.refresh(satellite)

    def update(self, id:int, satellite: Satellite, db:scoped_session) -> Satellite:
        satellite.id = id
        db.merge(satellite)
        db.commit()

    def delete(self, satellite: Satellite, db:scoped_session) -> None:
        db.delete(satellite)
        db.commit()
        db.flush()
    
    def search_by_norad_id(self, norad_id: int, db:scoped_session) -> Satellite:
        s = db.query(Satellite).filter_by(norad_id=norad_id).first()
        return s

    def search_by_name(self, key: str, db:scoped_session) -> List[Satellite]:
        s = db.query(Satellite).filter(Satellite.name.ilike("%{0}%".format(key))).all()
        return s
    
    def getById(self, id: int, db:scoped_session) -> Satellite:
        s= db.query(Satellite).get(id)
        return s
    
satellite_repository = SatelliteRepository()

def get_satellite_repository():
    return satellite_repository
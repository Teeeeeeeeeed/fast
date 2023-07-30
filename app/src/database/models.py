from sqlalchemy import Column, DateTime, Integer, MetaData, PrimaryKeyConstraint, String, func
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Satellite(Base):
    __tablename__ = "satellites"

    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    transaction_count = Column(String(200))
    norad_id = Column(Integer, unique=True)
    tle = Column(String(200))
    create_at = Column(DateTime, default=func.now())

    PrimaryKeyConstraint(id)

    def __repr__(self):
        return f"id:{self.id} satellite name:{self.name}"
    

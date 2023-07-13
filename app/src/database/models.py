from sqlalchemy import Column, DateTime, Integer, MetaData, String, func
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base(metadata=MetaData(schema="myschema"))

class Satellite(Base):
    __tablename__ = "satellites"

    id = Column(Integer, primary_key=True)
    name = Column(String(60), unique=True)
    norad_id = Column(Integer)
    transaction_count = Column(String(200))
    tle = Column(String(200))
    create_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"id:{self.id} satellite name:{self.name}"
    
    
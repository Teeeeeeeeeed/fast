from sqlalchemy import create_engine
from dotenv import dotenv_values
from sqlalchemy.orm import sessionmaker, scoped_session

env = dotenv_values(".env")
SQLALCHEMY_DATABASE_URL = env['SQLALCHEMY_DATABASE_URL']
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
LocalSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db_connection():
    db = scoped_session(LocalSession)
    try:
        yield db
    finally:
        db.close()
import os
from sqlalchemy import create_engine
from dotenv import dotenv_values, load_dotenv
from sqlalchemy.orm import sessionmaker, scoped_session

load_dotenv()

db_url = os.environ.get("SQLALCHEMY_DATABASE_URL")
engine = create_engine(db_url, echo=True)
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
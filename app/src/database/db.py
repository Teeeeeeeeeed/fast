from sqlalchemy import create_engine
from dotenv import dotenv_values

env = dotenv_values(".env")
SQLALCHEMY_DATABASE_URL = env['SQLALCHEMY_DATABASE_URL']
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
Session = sessionmaker
with session as conn:
    print("connected")
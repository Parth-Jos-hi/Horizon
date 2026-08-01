from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

## this will create a connection b/w the sql and the database 
engine = create_engine(
    settings.DATABASE_URL
    ,echo = True
)


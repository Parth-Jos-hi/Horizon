from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
## this will create a connection b/w the sql and the database 
engine = create_engine(
    "postgresql+psycopg2://postgres:Imparth@12_12@db.fhsvahlkqpxyzrylrcna.supabase.co:5432/postgres"
    ,echo = True
)

from sqlalchemy import create_engine
engine = create_engine(
    "postgresql+psycopg2://postgres:Imparth@12_12@db.fhsvahlkqpxyzrylrcna.supabase.co:5432/postgres"
    ,echo = True
)
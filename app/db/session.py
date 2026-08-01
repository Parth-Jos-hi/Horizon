from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,autocommit
from app.config import settings

## this will create a connection b/w the sql and the database 
engine = create_engine(
    settings.DATABASE_URL
    ,echo = True
)
SessionLocal = sessionmaker(
    ## bind tell the session maker that which engine to use for session maker
    bind = engine,
    ## it will not auto changes the commits after each operation
    ## only after session.commit it will commit the changes
    autocommit = False,
    ## it will take the new query and jot it down in the temporary memory till we comming session.commit() 
    # but it will be shown in the database when we search anything
    autoflush =True
)


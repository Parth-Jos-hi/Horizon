from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
# here we will create a declarative base class that our models will inherit from 
class Base(DeclarativeBase):
    pass



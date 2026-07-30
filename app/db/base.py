from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column,String
from sqlalchemy import String
# here we will create a declarative base class that our models will inherit from 
class base(DeclarativeBase):
    pass
class Users(base):
    _Tablename_ = "user-info"
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str]= mapped_column(String(30),nullable= False)
    email:Mapped[str]= mapped_column(unique=True)



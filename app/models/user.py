from app.db.base import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String
import enum
from sqlalchemy import Enum
from sqlalchemy.types import UUID
import uuid
import datetime
class roles(enum.Enum):
    admin = "admin"
    user = "user"
class Users(Base):
    __tablename__ = "users"
    id:Mapped[int] = mapped_column(primary_key=True,as_uuid = True)
    name:Mapped[str]= mapped_column(String(30),nullable= False)
    email:Mapped[str]= mapped_column(String(255),unique=True,nullable=False)
    password_hash:Mapped[str]= mapped_column(String(255),nullable = False)
    role:Mapped[roles] = mapped_column(Enum(roles),nullable = False,default = roles.user)
    created_at:Mapped[datetime.datetime]=mapped_column(default = datetime.datetime.now)
    updated_at:Mapped[datetime.datetime.now] = mapped_column(default = datetime.datetime.now)
    def __repr__(self)->str:
        return f"User(id= {self.id!r},name={self.name!r},email={self.email!r})"
    

from app.db.base import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String
class Users(Base):
    __tablename__ = "user"
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str]= mapped_column(String(30),nullable= False)
    email:Mapped[str]= mapped_column(String(255),unique=True,nullable=False)
    def __repr__(self)->str:
        return f"User(id= {self.id!r},name={self.name!r},email={self.email!r})"

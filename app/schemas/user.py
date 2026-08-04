from uuid import UUID
from pydantic import EmailStr,BaseModel,SecretStr,Field,ConfigDict
from typing import Optional
from datetime import datetime
from app.models.user import UserRole
class Userbase(BaseModel):
    email:EmailStr
class UserCreate(BaseModel):
    password:SecretStr= Field(min_length = 8)
    display_name:str = Field(max_length = 50)
class UserLogin(BaseModel):
    password:SecretStr
class UserUpdate(BaseModel):
    email:Optional[EmailStr] = None
    password:Optional[SecretStr] = Field(default = None,min_length=8)
    display_name:Optional[str] = Field(default = None,min_length=50)
class UserResponse(BaseModel):
    id:UUID
    email:EmailStr
    display_name:str
    role:UserRole
    created_at:datetime
    model_config = ConfigDict(from_attributes=True)
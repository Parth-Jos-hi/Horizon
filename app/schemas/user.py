from pydantic import EmailStr,BaseModel,SecretStr
from typing import Optional,Field
from datetime import datetime,timezone
class UserCreate(BaseModel):
    email:EmailStr
    password:SecretStr
    display_name:str
class UserLogin(BaseModel):
    email:EmailStr
    password:SecretStr
class UserUpdate(BaseModel):
    email:Optional[EmailStr] = None
    password:Optional[SecretStr] = None
    display_name:Optional[str] = None
class UserResponse(BaseModel):
    id:str
    email:EmailStr
    display_name:str
    role:str
    created_at:datetime = Field(default_factory=lambda:datetime.now(timezone.utc))

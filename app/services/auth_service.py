from typing import Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session  
from app.models.user import User
from app.schemas.user import UserCreate , UserResponse
from app.core.security import hash_password,verify_password
def register_user(session:Session,data:UserCreate) ->UserResponse:
    existing = session.execute(
        select(User).where(User.email== data.email)
    ).scalar_one_or_none()
    if existing is not None:
        raise ValueError("An account with this email already exists")
    user = User(
        email=data.email,
        display_name=data.display_name,
        password_hash=hash_password(data.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return UserResponse.model_validate(user)
def authenticate_user(session:Session,email:str,password:str) ->Optional[User]:
    user = session.execute(
        select(User).where(User.email == email)
    ).scalar_one_or_none()
    if user is None:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user

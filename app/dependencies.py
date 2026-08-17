from fastapi.security import OAuth2PasswordBearer
from typing import Generator
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import Depends , HTTPException ,status
from app.models.user import User
from app.db.session import SessionLocal
from app.core.security import decode_access_token
from sqlalchemy import select
import jwt
oauth2_scheme =OAuth2PasswordBearer(tokenUrl ="/api/v1/auth/login")
def get_db()->Generator[Session,None,None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def get_current_user(
        token:str = Depends(oauth2_scheme),
        db:Session = Depends(get_db),
)->User:
    credentials_error = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentails",
        headers={"WWW-Authenticate":"Bearer"},
    )
    try:
        payload = decode_access_token(token)
    except jwt.ExpiredSignatureError:
        raise  HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Token has expired",
            headers = {"WWW-Authenticate":"Bearer"},
        )
    except jwt.InvalidTokenError:
        raise credentials_error
    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_error
    user = db.execute(
        select(User).where(User.id==UUID(user_id))
    ).scalar_one_or_none()
    if user is None:
        raise credentials_error
    return user
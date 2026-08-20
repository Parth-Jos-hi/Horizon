from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import register_user, authenticate_user
from app.core.security import create_access_token
from app.models.user import User
router = APIRouter()
@router.post("/auth/register",response_model = UserResponse,status_code=status.HTTP_201_CREATED,)
def register(data:UserCreate,db:Session=Depends(get_db)):
    try:    
        return register_user(data, db)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail = str(e))

@router.post("/auth/login")
def login(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db),):
    user = authenticate_user(db,form_data.username,form_data.password)
    if user is None:
        raise HTTPException(
            stauts_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(user.id)
    return {"access_token":access_token,"token_type":"bearer"}
@router.get("/user/profile",response_model = UserResponse)
def get_profile(current_user:User=Depends(get_current_user)):
    return current_user

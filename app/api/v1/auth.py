from fastapi import FastAPI
from pydantic import SecretStr
from app.services.auth_service import register_user
from app.dependencies import get_current_user
from sqlalchemy.orm import Session
app = FastAPI()
@app.post("/register")
def register_user(display_name:str,password:SecretStr):
    return register_user(display_name, password)
@app.get("login")
async def UserLogin(token:str,db:Session):
    return get_current_user(token,db)
from fastapi import FastAPI
from pydantic import SecretStr
from app.services.auth_service import register_user
app = FastAPI()
@app.post("/login")
def register_user(display_name:str,password:SecretStr):
    return register_user(display_name, password)

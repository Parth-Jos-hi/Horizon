from app.api.v1 import auth,data
from fastapi import APIRouter
routers = APIRouter()
routers.include_router(auth.router
            ,prefix = "/api/v1",
            tags = ["auth"])
routers.include_router(data.router,
            prefix = "/api/v1",
            tags = ["data"])
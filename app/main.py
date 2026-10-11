from fastapi import FastAPI
from app.api.v1.router import routers
app = FastAPI(
    title="Horizon",
    version="0.1",
)
app.include_router(routers)


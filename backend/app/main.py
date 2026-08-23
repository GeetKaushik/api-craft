#Starts the application

from contextlib import asynccontextmanager

from fastapi import  FastAPI
from sqlmodel import SQLModel, Session

from app.database.database import engine
from app.database import models
from app.database.dependencies import get_session
from app.routers import users

@asynccontextmanager #This function manages resources for the application's lifetime
async def lifespan(app:FastAPI):
    # SQLModel.metadata.create_all(engine)
    yield

app=FastAPI(
    lifespan=lifespan
)

app.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]
)


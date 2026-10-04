#Starts the application
from dotenv import load_dotenv

load_dotenv()

from contextlib import asynccontextmanager
from fastapi import  FastAPI
from sqlmodel import SQLModel, Session
from app.database.database import engine
from app.database import models
from app.database.dependencies import get_session
from app.routers import users,ai,dynamic
from app.routers.ai import router as ai_router


@asynccontextmanager #This function manages resources for the application's lifetime
async def lifespan(app:FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app=FastAPI(
    lifespan=lifespan
)

app.include_router(
    users.router,
    tags=["Users"]
)

app.include_router(ai_router)
app.include_router(dynamic.router)

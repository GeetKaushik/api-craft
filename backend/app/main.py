#Starts the application

from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

from app.database.database import engine
from app.database import models

@asynccontextmanager #This function manages resources for the application's lifetime
async def lifespan(app:FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app=FastAPI(
    lifespan=lifespan
)
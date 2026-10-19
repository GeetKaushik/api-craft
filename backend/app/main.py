from dotenv import load_dotenv

load_dotenv()

from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel, Session, select

from app.database.database import engine
from app.database import models
from app.database.models import GeneratedAPI
from app.routers import users, ai, dynamic, auth,generated_apis
from app.routers.ai import router as ai_router
from app.services.schema_service import (
    create_dynamic_model,
    register_dynamic_model,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create missing application tables.
    SQLModel.metadata.create_all(engine)

    # Restore only APIs explicitly saved in generated_api.
    with Session(engine) as session:
        saved_apis = session.exec(select(GeneratedAPI)).all()

        for api_definition in saved_apis:
            try:
                from app.schemas.api_schema import APISchema

                api_schema = APISchema.model_validate_json(
                    api_definition.api_schema_json
                )

                dynamic_model = create_dynamic_model(
                    api_schema,
                    table_name=api_definition.table_name,
                )

                register_dynamic_model(dynamic_model)

                print(
                    "RESTORED USER API:",
                    f"user_id={api_definition.owner_id},",
                    f"resource={api_definition.resource_name},",
                    f"table={api_definition.table_name}",
                )

            except Exception as exc:
                print(
                    "FAILED TO RESTORE API:",
                    api_definition.resource_name,
                    repr(exc),
                )

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(users.router, tags=["Users"])
app.include_router(ai_router)
app.include_router(dynamic.router)
app.include_router(auth.router)
app.include_router(generated_apis.router)

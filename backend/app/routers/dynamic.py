from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.database.dependencies import get_session
from app.services.schema_service import get_dynamic_model, create_dynamic_request_model
from app.services.dynamic_service import (
    create_dynamic_record,
    get_dynamic_records as get_records,
)

router = APIRouter(prefix="/dynamic", tags=["Dynamic APIs"])


@router.post("/{resource_name}")
def create_record(
    resource_name: str, data: dict, session: Session = Depends(get_session)
):
    """
    Creates a record in a dynamically generated resource.
    """

    dynamic_model = get_dynamic_model(resource_name)

    if dynamic_model is None:
        raise HTTPException(
            status_code=404, detail=f"Dynamic resource '{resource_name}' not found"
        )

    record = create_dynamic_record(
        session=session, dynamic_model=dynamic_model, data=data
    )

    return record


def register_dynamic_routes(app, api_schema, dynamic_model):
    """
    Registers concrete FastAPI routes for an AI-generated resource.
    """

    resource_name = api_schema.resource_name

    # Create Pydantic request model dynamically
    request_model = create_dynamic_request_model(api_schema)

    print("GENERATED REQUEST MODEL:", request_model)

    # -------------------------
    # POST /dynamic/{resource}
    # -------------------------
    def create_dynamic_record_endpoint(data, session: Session = Depends(get_session)):
        record = create_dynamic_record(
            session=session, dynamic_model=dynamic_model, data=data.model_dump()
        )

        return record

    # Tell FastAPI about the dynamically
    # generated request model
    create_dynamic_record_endpoint.__annotations__["data"] = request_model

    app.add_api_route(
        f"/dynamic/{resource_name}",
        create_dynamic_record_endpoint,
        methods=["POST"],
        tags=["Generated APIs"],
        name=f"Create {resource_name}",
    )

    # Clear cached OpenAPI schema
    app.openapi_schema = None

    print("REGISTERED API ROUTE:", f"/dynamic/{resource_name}")


@router.get("/{resource_name}")
def get_dynamic_records(resource_name: str, session: Session = Depends(get_session)):
    dynamic_model = get_dynamic_model(resource_name)
    if not dynamic_model:
        raise HTTPException(
            status_code=404, detail=f"Resource '{resource_name}' not found"
        )
    return get_records(session, dynamic_model)

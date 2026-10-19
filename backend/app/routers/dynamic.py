from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.database.dependencies import get_session
from app.database.models import User
from app.auth_dependencies import get_current_user
from app.services.generated_api_service import get_owned_api
from app.services.schema_service import (
    get_dynamic_model,
    create_dynamic_model,
)
from app.schemas.api_schema import APISchema
from app.services.dynamic_service import (
    create_dynamic_record,
    get_dynamic_records as get_records,
)

router = APIRouter(prefix="/dynamic", tags=["Dynamic APIs"])


def get_user_dynamic_model(
    session: Session,
    current_user: User,
    resource_name: str,
):
    # Find this API only if it belongs to the logged-in user.
    api_definition = get_owned_api(
        session=session,
        owner_id=current_user.id,
        resource_name=resource_name,
    )

    if api_definition is None:
        raise HTTPException(
            status_code=404,
            detail=f"Resource '{resource_name}' not found.",
        )

    if api_definition.is_archived:
        raise HTTPException(
            status_code=404,
            detail=f"Resource '{resource_name}' not found.",
        )

    # Reconstruct the schema saved when this API was generated.
    api_schema = APISchema.model_validate_json(api_definition.api_schema_json)

    # Use the user's physical database table, e.g. user_2_products.
    dynamic_model = get_dynamic_model(api_definition.table_name)

    # Rebuild the model if it isn't registered in memory.
    if dynamic_model is None:
        dynamic_model = create_dynamic_model(
            api_schema,
            table_name=api_definition.table_name,
        )

    return dynamic_model


@router.post("/{resource_name}")
def create_record(
    resource_name: str,
    data: dict,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Creates a record in a dynamically generated resource.
    """

    dynamic_model = get_user_dynamic_model(session, current_user, resource_name)
    return create_dynamic_record(session, dynamic_model, data)


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
def get_dynamic_records(
    resource_name: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    dynamic_model = get_user_dynamic_model(session, current_user, resource_name)
    return get_records(session, dynamic_model)



@router.get("/{resource_name}/{record_id}")
def get_dynamic_record_by_id(
    resource_name: str,
    record_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    dynamic_model = get_user_dynamic_model(
        session, current_user, resource_name
    )

    record = session.get(dynamic_model, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found.")

    return record


@router.delete("/{resource_name}/{record_id}", status_code=204)
def delete_dynamic_record(
    resource_name: str,
    record_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    dynamic_model = get_user_dynamic_model(
        session, current_user, resource_name
    )

    record = session.get(dynamic_model, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found.")

    session.delete(record)
    session.commit()
    return None


@router.patch("/{resource_name}/{record_id}")
def update_dynamic_record(
    resource_name: str,
    record_id: int,
    data: dict,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    dynamic_model = get_user_dynamic_model(
        session, current_user, resource_name
    )

    record = session.get(dynamic_model, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found.")

    allowed_fields = set(dynamic_model.model_fields.keys()) - {"id"}
    invalid_fields = set(data.keys()) - allowed_fields

    if invalid_fields:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid fields: {', '.join(sorted(invalid_fields))}",
        )

    for field, value in data.items():
        setattr(record, field, value)

    session.add(record)
    session.commit()
    session.refresh(record)
    return record

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database.dependencies import get_session
from app.database.models import User, GeneratedAPI
from app.auth_dependencies import get_current_user
from app.services.generated_api_service import (
    list_owned_apis,
    get_owned_api,
)
from app.schemas.api_schema import APISchema

router = APIRouter(prefix="/apis", tags=["Generated APIs"])


def set_api_archived_status(
    session: Session,
    owner_id: int,
    resource_name: str,
    is_archived: bool,
):
    api = session.exec(
        select(GeneratedAPI).where(
            GeneratedAPI.owner_id == owner_id,
            GeneratedAPI.resource_name == resource_name,
        )
    ).first()

    if api is None:
        raise HTTPException(
            status_code=404,
            detail=f"API '{resource_name}' not found.",
        )

    api.is_archived = is_archived
    session.add(api)
    session.commit()
    session.refresh(api)

    return api


@router.get("/")
def list_generated_apis(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    # Fetch only APIs belonging to the logged-in user.
    apis = list_owned_apis(
        session=session,
        owner_id=current_user.id,
    )

    return [
        {
            "id": api.id,
            "resource_name": api.resource_name,
            "description": api.description,
            "endpoint": f"/dynamic/{api.resource_name}",
            "schema": APISchema.model_validate_json(api.api_schema_json).model_dump(),
            "created_at": api.created_at,
        }
        for api in apis
    ]


@router.get("/{resource_name}")
def get_generated_api(
    resource_name: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    # Look up the API using both its name and its owner's ID.
    api = get_owned_api(
        session=session,
        owner_id=current_user.id,
        resource_name=resource_name,
    )

    if api is None:
        raise HTTPException(
            status_code=404,
            detail=f"API '{resource_name}' not found.",
        )
    if api.is_archived:
        raise HTTPException(
            status_code=404,
            detail=f"API '{resource_name}' not found.",
        )

    return {
        "id": api.id,
        "resource_name": api.resource_name,
        "description": api.description,
        "endpoint": f"/dynamic/{api.resource_name}",
        "schema": APISchema.model_validate_json(api.api_schema_json).model_dump(),
        "created_at": api.created_at,
    }


@router.patch("/{resource_name}/archive")
def archive_generated_api(
    resource_name: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    api = set_api_archived_status(
        session=session,
        owner_id=current_user.id,
        resource_name=resource_name,
        is_archived=True,
    )

    return {
        "message": f"API '{resource_name}' archived successfully.",
        "resource_name": api.resource_name,
        "is_archived": api.is_archived,
    }


@router.patch("/{resource_name}/restore")
def restore_generated_api(
    resource_name: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    api = set_api_archived_status(
        session=session,
        owner_id=current_user.id,
        resource_name=resource_name,
        is_archived=False,
    )

    return {
        "message": f"API '{resource_name}' restored successfully.",
        "resource_name": api.resource_name,
        "is_archived": api.is_archived,
    }

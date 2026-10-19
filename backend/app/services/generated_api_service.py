# Generates physical table names such as user_1_products and user_2_products.
# Finds an API using both owner_id and resource_name.
# Lists only a user's own API definitions.
# Saves the schema as JSON so it can be reconstructed after a restart.
import re

from sqlmodel import Session, select

from app.database.models import GeneratedAPI
from app.schemas.api_schema import APISchema


def make_table_name(owner_id: int, resource_name: str) -> str:
    """Create a unique, safe physical table name for a user's API."""

    safe_name = resource_name.lower()

    if not re.fullmatch(r"[a-z][a-z0-9_]{0,79}", safe_name):
        raise ValueError(
            "Resource names must start with a letter and contain "
            "only lowercase letters, numbers, and underscores."
        )

    return f"user_{owner_id}_{safe_name}"


def get_owned_api(
    session: Session,
    owner_id: int,
    resource_name: str,
) -> GeneratedAPI | None:
    """Find an API definition belonging to a particular user."""

    statement = select(GeneratedAPI).where(
        GeneratedAPI.owner_id == owner_id,
        GeneratedAPI.resource_name == resource_name,
    )

    return session.exec(statement).first()


def list_owned_apis(
    session: Session,
    owner_id: int,
) -> list[GeneratedAPI]:
    """List only the API definitions belonging to a user."""

    statement = select(GeneratedAPI).where(
        GeneratedAPI.owner_id == owner_id,
        GeneratedAPI.is_archived == False,
    )

    return list(session.exec(statement).all())


def save_api_definition(
    session: Session,
    owner_id: int,
    api_schema: APISchema,
    table_name: str,
) -> GeneratedAPI:
    """Save a generated API schema and associate it with its owner."""

    existing = get_owned_api(
        session,
        owner_id,
        api_schema.resource_name,
    )

    if existing is not None:
        raise ValueError(f"You already have an API named '{api_schema.resource_name}'.")

    api_definition = GeneratedAPI(
        owner_id=owner_id,
        resource_name=api_schema.resource_name,
        table_name=table_name,
        description=api_schema.description,
        api_schema_json=api_schema.model_dump_json(),
    )

    session.add(api_definition)
    session.commit()
    session.refresh(api_definition)

    return api_definition

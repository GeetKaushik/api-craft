
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session

from app.database.dependencies import get_session
from app.database.models import User
from app.auth_dependencies import get_current_user

from app.schemas.ai import AIRequest, AIResponse
from app.schemas.api_schema import APIRequest, APISchema

from app.services.ai_service import (
    generate_ai_analysis,
    generate_api_schema,
)

from app.services.schema_service import (
    interpret_api_schema,
    create_database_table,
    create_dynamic_model,
    register_dynamic_model,
    get_dynamic_model,
)

from app.services.database_inspector import (
    table_exists,
    get_existing_api_schema,
    apply_minor_changes,
    apply_major_change,
)

from app.services.schema_comparator import compare_schemas

from app.services.generated_api_service import (
    make_table_name,
    get_owned_api,
    save_api_definition,
)


router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)

@router.post("/analyze", response_model=AIResponse)
def analyze_content(data: AIRequest):

    try:
        result = generate_ai_analysis(
            data.title,
            data.content
        )

        print("RESULT FROM AI SERVICE:", result)
        print("RESULT TYPE:", type(result))
        validated_result= AIResponse.model_validate(result)
        print("VALIDATED RESULT:",validated_result)
        return validated_result

    except Exception as e:
        import traceback

        print("GEMINI ERROR:", repr(e))
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.post("/generate-schema", response_model=APISchema)
def generate_schema(
    request: Request,
    data: APIRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    try:
        # 1. Generate and validate the schema.
        result = generate_api_schema(data.prompt)
        validated_result = APISchema.model_validate(result)

        print("VALIDATED API SCHEMA:", validated_result)

        # 2. Validate the resource name and create a user-specific table name.
        try:
            table_name = make_table_name(
                current_user.id,
                validated_result.resource_name,
            )
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc))

        # 3. Check whether this user already owns an API with this name.
        existing_api = get_owned_api(
            session,
            current_user.id,
            validated_result.resource_name,
        )

        if existing_api is not None:
            raise HTTPException(
                status_code=409,
                detail=(
                    f"You already have an API named "
                    f"'{validated_result.resource_name}'. "
                    "Use a different resource name for now."
                ),
            )

        # 4. Create the dynamic model using the user-specific table name.
        dynamic_model = create_dynamic_model(
            validated_result,
            table_name=table_name,
        )

        # 5. Create the physical database table.
        create_database_table(dynamic_model)

        # 6. Save the API definition and its owner.
        try:
            save_api_definition(
                session=session,
                owner_id=current_user.id,
                api_schema=validated_result,
                table_name=table_name,
            )
        except Exception:
            session.rollback()
            raise

        # 7. Register the model by its physical table name.
        register_dynamic_model(dynamic_model)

        print("DATABASE TABLE CREATED:", table_name)
        print("API OWNER ID:", current_user.id)

        return validated_result

    except HTTPException:
        raise

    except Exception as exc:
        import traceback

        print("API SCHEMA GENERATION ERROR:", repr(exc))
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail="Failed to generate the API schema.",
        ) from exc

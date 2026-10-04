from fastapi import APIRouter, HTTPException,Request

from app.schemas.ai import AIRequest,AIResponse
from app.schemas.api_schema import APIRequest,APISchema
from app.services.ai_service import (generate_ai_analysis,generate_api_schema)
from app.services.schema_service import (interpret_api_schema,create_database_table,create_dynamic_model,register_dynamic_model)

from app.routers.dynamic import register_dynamic_routes

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
def generate_schema(request:Request, data: APIRequest):
    try:
        # 1. Ask Gemini to generate the API schema
        result = generate_api_schema(data.prompt)

        print("GENERATED API SCHEMA:", result)

        # 2. Validate Gemini's response using Pydantic
        validated_result = APISchema.model_validate(result)

        print("VALIDATED API SCHEMA:", validated_result)

        # 3. Interpret the schema
        interpreted_result = interpret_api_schema(validated_result)

        print("INTERPRETED API SCHEMA:", interpreted_result)

        # 4. Create a dynamic SQLModel class
        dynamic_model = create_dynamic_model(validated_result)

        print("DYNAMIC MODEL:", dynamic_model)
        print("TABLE NAME:", dynamic_model.__tablename__)

        # 5. Create the table in SQL Server
        create_database_table(dynamic_model)

        print("DATABASE TABLE CREATED")

        # 6. Register the model so the dynamic CRUD routes
        #    can find it later
        register_dynamic_model(dynamic_model)

        print("REGISTERED MODEL:", dynamic_model.__tablename__)

        # 7. Register FastAPI routes
        register_dynamic_routes(
            app=request.app,
            api_schema=validated_result,
            dynamic_model=dynamic_model
        )
        print("REGISTERED API ROUTE:",f"/dynamic/{validated_result.resource_name}")

        # 8. Return the validated schema to the frontend
        return validated_result

    except Exception as e:
        import traceback

        print("API SCHEMA GENERATION ERROR:", repr(e))
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
   
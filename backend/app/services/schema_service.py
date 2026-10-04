from sqlmodel import SQLModel, Field
from pydantic import create_model
from sqlmodel.main import SQLModelMetaclass
from app.database.database import engine

TYPE_MAPPING = {
    "string": str,
    "integer": int,
    "float": float,
    "boolean": bool,
}  # Gemini return in "string and it is converting it to str in python type"

DYNAMIC_MODELS = {}# Registery


def get_python_type(field_type: str):

    if field_type not in TYPE_MAPPING:
        raise ValueError(f"Unsupported field type: {field_type}")

    return TYPE_MAPPING[field_type]


def interpret_api_schema(api_schema):

    interpreted_fields = []

    for field in api_schema.fields:

        python_type = get_python_type(field.type)

        interpreted_fields.append(
            {"name": field.name, "python_type": python_type, "required": field.required}
        )

    return {
        "resource_name": api_schema.resource_name,
        "description": api_schema.description,
        "fields": interpreted_fields,
    }


def create_dynamic_model(api_schema):
    """
    Dynamically creates a SQLModel table class
    from an APISchema object.
    """

    model_name = api_schema.resource_name.capitalize()

    annotations = {"id": int | None}

    namespace = {
        "__annotations__": annotations,
        "id": Field(default=None, primary_key=True),
    }

    for field in api_schema.fields:

        python_type = get_python_type(field.type)

        if field.required:
            annotations[field.name] = python_type

        else:
            annotations[field.name] = python_type | None
            namespace[field.name] = Field(default=None)

    namespace["__tablename__"] = api_schema.resource_name

    DynamicModel = SQLModelMetaclass(model_name, (SQLModel,), namespace, table=True)

    return DynamicModel

def create_dynamic_request_model(api_schema):
    """
    Creates a dynamic Pydantic model for the API request body.

    This model is used by FastAPI to generate
    the correct Swagger/OpenAPI request schema.
    """

    fields = {}

    for field in api_schema.fields:

        python_type = get_python_type(field.type)

        if field.required:
            fields[field.name] = (
                python_type,
                Field(...)
            )
        else:
            fields[field.name] = (
                python_type | None,
                Field(default=None)
            )

    RequestModel = create_model(
        f"{api_schema.resource_name.capitalize()}Request",
        **fields
    )

    return RequestModel

def register_dynamic_model(dynamic_model):
    """
    Stores a dynamically generated model
    so it can be retrieved later.
    """

    table_name = dynamic_model.__tablename__

    DYNAMIC_MODELS[table_name] = dynamic_model

    return dynamic_model


def get_dynamic_model(resource_name: str):
    """
    Retrieves a dynamically generated model
    using its resource name.
    """

    return DYNAMIC_MODELS.get(resource_name)


def create_database_table(dynamic_model):
    """
    Creates the SQL Server table for the dynamically generated model.
    """

    dynamic_model.metadata.create_all(engine, tables=[dynamic_model.__table__])

    return dynamic_model


if __name__ == "__main__":

    from app.schemas.api_schema import APISchema, APIField

    test_schema = APISchema(
        resource_name="products",
        description="E-commerce product API",
        fields=[
            APIField(name="product_name", type="string", required=True),
            APIField(name="price", type="float", required=True),
            APIField(name="ratings", type="float", required=False),
            APIField(name="in_stock", type="boolean", required=True),
        ],
    )

    ProductModel = create_dynamic_model(test_schema)
    register_dynamic_model(ProductModel)
    print("MODEL:", ProductModel)
    print("MODEL NAME:", ProductModel.__name__)
    print("TABLE NAME:", ProductModel.__tablename__)
    print("ANNOTATIONS:", ProductModel.__annotations__)

    print("\nDATABASE COLUMNS:")

    for column in ProductModel.__table__.columns:
        print(
            column.name,
            "->",
            column.type,
            "| nullable:",
            column.nullable,
            "| primary_key:",
            column.primary_key,
        )

    # Create the table in SQL Server
    create_database_table(ProductModel)

    print("\nDATABASE TABLE CREATED SUCCESSFULLY!")

    print("\nREGISTERED MODELS:")
    print(DYNAMIC_MODELS)

    print("\nRETRIEVED MODEL:")
    print(get_dynamic_model("products"))

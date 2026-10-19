from sqlalchemy import inspect, text

from app.database.database import engine
from app.schemas.api_schema import APIField, APISchema
from app.services.schema_comparator import compare_schemas
from app.services.schema_service import (
    create_dynamic_model,
    create_database_table,
    register_dynamic_model,
    interpret_api_schema,
)


def table_exists(table_name: str) -> bool:
    """
    Checks whether a table exists in the APICraft SQL Server database.
    """

    inspector = inspect(engine)

    return inspector.has_table(table_name)


def get_next_versioned_table_name(table_name: str) -> str:
    """
    Generate the next available versioned table name.

    Example:
        products -> products_v2
        products_v2 already exists -> products_v3
    """

    version = 2

    while True:
        versioned_name = f"{table_name}_v{version}"

        if not table_exists(versioned_name):
            return versioned_name

        version += 1


def create_versioned_table(new_schema):
    """
    Create a new versioned table for a MAJOR schema change.

    The existing table is never modified or deleted.
    """

    old_table_name = new_schema.resource_name

    versioned_table_name = get_next_versioned_table_name(old_table_name)

    # Create a copy of the schema with the versioned table name
    versioned_schema = new_schema.model_copy(
        update={"resource_name": versioned_table_name}
    )

    return versioned_schema


def apply_major_change(new_schema):
    """
    Create a new versioned table for a MAJOR schema change.

    The existing table remains untouched.
    """

    versioned_schema = create_versioned_table(new_schema)

    return versioned_schema


def get_table_columns(table_name: str):
    """
    Returns information about the columns of an existing table.
    """

    inspector = inspect(engine)

    if not inspector.has_table(table_name):
        return None

    return inspector.get_columns(table_name)


def sql_type_to_api_type(sql_type) -> str:
    """
    Convert SQLAlchemy/SQL Server column types
    into APICraft API schema types.
    """

    type_name = str(sql_type).upper()

    # String types
    if any(t in type_name for t in [
        "CHAR", "TEXT", "CLOB", "XML", "UNIQUEIDENTIFIER"
    ]):
        return "string"

    # Integer types
    if any(t in type_name for t in [
        "BIGINT", "SMALLINT", "TINYINT", "INTEGER", "INT"
    ]):
        return "integer"

    # Floating-point types
    if any(t in type_name for t in [
        "FLOAT", "REAL"
    ]):
        return "float"

    # Decimal / numeric types
    if any(t in type_name for t in [
        "DECIMAL", "NUMERIC", "MONEY"
    ]):
        return "float"

    # Boolean type
    if "BIT" in type_name:
        return "boolean"

    # Date and time types
    if any(t in type_name for t in [
        "DATETIMEOFFSET",
        "DATETIME2",
        "SMALLDATETIME",
        "DATETIME",
        "TIMESTAMP",
        "DATE",
        "TIME",
    ]):
        return "string"

    # Other common SQL Server types
    if "BINARY" in type_name or "IMAGE" in type_name:
        return "string"

    raise ValueError(f"Unsupported SQL Server type: {type_name}")

def add_column_to_table(
    table_name: str, column_name: str, column_type: str, nullable: bool = True
):
    """
    Add a new column to an existing SQL Server table.
    """
    SQL_TYPE_MAPPING = {
        "string": "VARCHAR(255)",
        "integer": "INTEGER",
        "float": "FLOAT",
        "boolean": "BIT",
    }
    if column_type not in SQL_TYPE_MAPPING:
        raise ValueError(f"Unsupported API field type:{column_type}")

    sql_type = SQL_TYPE_MAPPING[column_type]

    nullability = "NULL" if nullable else "NOT NULL"

    query = text(
        f"ALTER TABLE [{table_name}] " f"ADD [{column_name}] {sql_type} {nullability}"
    )

    with engine.begin() as connection:
        connection.execute(query)

    return {
        "table": table_name,
        "column": column_name,
        "type": column_type,
        "nullable": nullable,
    }


def apply_minor_changes(existing_schema, new_schema, comparison):
    """
    Apply safe MINOR schema changes to an existing SQL Server table.
    Preserve existing records.
    """

    table_name = existing_schema.resource_name

    existing_fields = {field.name: field for field in existing_schema.fields}

    new_fields = {field.name: field for field in new_schema.fields}

    applied_changes = []

    # 1. Add newly introduced fields
    for field_name in comparison["added_fields"]:
        field = new_fields[field_name]

        # A required new field needs a separate migration
        # strategy if the table already contains records.
        if field.required:
            raise ValueError(
                f"Cannot safely add required field '{field_name}' "
                "as a MINOR change. It needs a migration strategy."
            )

        add_column_to_table(
            table_name=table_name,
            column_name=field.name,
            column_type=field.type,
            nullable=True,
        )

        applied_changes.append(f"Added optional field: {field_name}")

    # 2. Change required fields to optional
    for field_name in comparison["changed_fields"]:
        old_field = existing_fields[field_name]
        new_field = new_fields[field_name]

        if old_field.required and not new_field.required:
            columns = get_table_columns(table_name)

            column = next(
                (item for item in columns if item["name"] == field_name),
                None,
            )

            if column is None:
                raise ValueError(
                    f"Column '{field_name}' was not found " f"in table '{table_name}'."
                )

            sql_type = column["type"].compile(dialect=engine.dialect)

            query = text(
                f"ALTER TABLE [{table_name}] "
                f"ALTER COLUMN [{field_name}] {sql_type} NULL"
            )

            with engine.begin() as connection:
                connection.execute(query)

            applied_changes.append(f"Changed field to optional: {field_name}")

    return {
        "change_type": "MINOR",
        "table": table_name,
        "applied_changes": applied_changes,
    }


def get_existing_api_schema(table_name: str) -> APISchema | None:
    """
    Read an existing database table and
    convert it into an APICraft APISchema.
    """
    columns = get_table_columns(table_name)
    if columns is None:
        return None
    fields = []
    print("\n BUILDING APISCHEMA:")
    for column in columns:
        # We dont want the primary key
        # to be compared with Gemini generated API fields.
        if column["name"] == "id":
            continue

        api_type = sql_type_to_api_type(column["type"])
        required = not column["nullable"]
        print("Creating APIField:", column["name"], api_type, required)
        api_field = APIField(name=column["name"], type=api_type, required=required)
        print("Created:", api_field)

        fields.append(api_field)

    print("\nFIELDS BEFORE APISCHEMA:")
    print(fields)

    result = APISchema(
        resource_name=table_name,
        description=f"Existing API Schema for {table_name}",
        fields=fields,
    )

    print("\nFIELDS AFTER APISCHEMA:")
    print(result.fields)

    return result

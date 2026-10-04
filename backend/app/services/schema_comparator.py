COMPATIBLE_TYPE_CHANGES = {
    ("integer", "float"),
}


def is_compatible_type_change(old_type, new_type):
    return (
        old_type == new_type
        or (old_type, new_type) in COMPATIBLE_TYPE_CHANGES
    )


def compare_schemas(existing_schema, new_schema):
    """
    Compares an existing API schema with a newly generated schema.

    Returns:
        {
            "change_type": "NO_CHANGE" | "MINOR" | "MAJOR",
            "added_fields": [],
            "removed_fields": [],
            "changed_fields": []
        }
    """

    existing_fields = {
        field.name: field
        for field in existing_schema.fields
    }

    new_fields = {
        field.name: field
        for field in new_schema.fields
    }

    added_fields = []
    removed_fields = []
    changed_fields = []

    major_change = False

    # -----------------------------------
    # 1. Detect added fields
    # -----------------------------------

    for field_name, new_field in new_fields.items():

        if field_name not in existing_fields:
            added_fields.append(field_name)

    # -----------------------------------
    # 2. Detect removed fields
    # -----------------------------------

    for field_name in existing_fields:

        if field_name not in new_fields:
            removed_fields.append(field_name)

            # Removing a field is major
            major_change = True

    # -----------------------------------
    # 3. Detect changed fields
    # -----------------------------------

    for field_name in existing_fields:

        if field_name not in new_fields:
            continue

        old_field = existing_fields[field_name]
        new_field = new_fields[field_name]

        type_changed = old_field.type != new_field.type
        required_changed = old_field.required != new_field.required

        if type_changed or required_changed:

            changed_fields.append(field_name)

            # -------------------------------
            # Required → Optional
            # -------------------------------

            if old_field.required and not new_field.required:

                # Safe: existing data remains valid
                continue

            # -------------------------------
            # Optional → Required
            # -------------------------------

            if not old_field.required and new_field.required:

                # Existing rows may contain NULL
                major_change = True
                continue

            # -------------------------------
            # Type change
            # -------------------------------

            if type_changed:

                if not is_compatible_type_change(
                    old_field.type,
                    new_field.type
                ):
                    major_change = True

    # -----------------------------------
    # 4. Decide final change type
    # -----------------------------------

    if not added_fields and not removed_fields and not changed_fields:

        change_type = "NO_CHANGE"

    elif major_change:

        change_type = "MAJOR"

    else:

        change_type = "MINOR"

    return {
        "change_type": change_type,
        "added_fields": added_fields,
        "removed_fields": removed_fields,
        "changed_fields": changed_fields,
    }


if __name__ == "__main__":

    from app.schemas.api_schema import APISchema, APIField

    existing_schema = APISchema(
        resource_name="products",
        description="Product API",
        fields=[
            APIField(
                name="name",
                type="string",
                required=True
            ),
            APIField(
                name="price",
                type="float",
                required=True
            ),
            APIField(
                name="ratings",
                type="float",
                required=True
            ),
        ],
    )

    new_schema = APISchema(
        resource_name="products",
        description="Updated Product API",
        fields=[
            APIField(
                name="name",
                type="string",
                required=True
            ),
            APIField(
                name="price",
                type="string",
                required=True
            ),
            APIField(
                name="ratings",
                type="float",
                required=False
            ),
            APIField(
                name="category",
                type="string",
                required=False
            ),
        ],
    )

    result = compare_schemas(
        existing_schema,
        new_schema
    )

    print(result)
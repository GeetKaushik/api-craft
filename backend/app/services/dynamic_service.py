from sqlmodel import Session,select


def create_dynamic_record(

    session: Session,
    dynamic_model,
    data: dict
):
    """
    Creates a record using a dynamically generated SQLModel.
    """

    record = dynamic_model(**data)

    session.add(record)
    session.commit()
    session.refresh(record)

    return record

def get_dynamic_records(
    session: Session,
    dynamic_model
):
    """
    Retrieves all records from a dynamically generated SQLModel table.
    """

    statement = select(dynamic_model)

    return session.exec(statement).all()
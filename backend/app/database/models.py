#SQL Model classes(Defines tables)

from typing import Optional

from sqlmodel import Field,SQLModel

# SQLModel: Connects Python code straight to a SQL database while checking data rules.
class User(SQLModel,table=True):
    id:Optional[int]=Field(default=None,primary_key=True)
    name:str
    email:str
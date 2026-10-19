from pydantic import BaseModel


class AIRequest(BaseModel):
    title: str
    content: str

class AIResponse(BaseModel):
    summary: str
    tags: list[str]
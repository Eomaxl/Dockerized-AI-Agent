from sqlmodel import SQLModel, Field

class ChatMessagePayload(SQLModel):
    # pydantic model
    # validation
    # serializer
    message: str

class ChatMessage(SQLModel, table=True):
    # database table
    # saving, updating, getting, deleting
    id: int | None = Field(default=None, primary_key=True)
    name: str
    message: str
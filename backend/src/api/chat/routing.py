from typing import List
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlmodel import Session, select

from api.db import get_session
from api.ai.services import generate_email_message
from api.chat.models import ChatMessageListItem
from .models import ChatMessagePayload, ChatMessage, ChatMessageListItem
router = APIRouter()

# /api/chats/
@router.get("/")
def chat_health():
    return {"status":"ok"}

# /api/chats/recent
# curl http://localhost:8080/api/chats/recent/
@router.get("/recent/",response_model=List[ChatMessageListItem])
def chat_list_messages(session: Session = Depends(get_session)):
    query = select(ChatMessage)
    results = session.exec(query).fetchall()[:10]
    return results

# background task to generate message
def process_ai_response(message_id: int, message: str):
    from api.db import engine
    with Session(engine) as session:
        try:
            response = generate_email_message(message)
            obj = session.get(ChatMessage, message_id)
            if obj:
                obj.response = response.message  # assuming response has .message
                obj.status = "done"
                session.add(obj)
                session.commit()
        except Exception as e:
            obj = session.get(ChatMessage, message_id)
            if obj:
                obj.response = str(e)
                obj.status = "failed"
                session.add(obj)
                session.commit()

# HTTP Post -> payload = {"message":"Hello World"} -> {"message":"hello world", "id": 1}
# curl -X POST -d '{"message":"Hello World"}' -H "Content-Type: application/json" http://localhost:8080/api/chats
# @router.post("/", response_model=EmailMessageSchema)
# def chat_create_message(
#     payload:ChatMessagePayload,
#     session: Session = Depends(get_session)
#     ):
#     data = payload.model_dump()
#     print(data)
#     obj = ChatMessage.model_validate(data)
#     session.add(obj)
#     session.commit()
#     # session.refresh(obj) # ensure id/primary key added to the obj instance
#     # ready to store in the database
#     response = generate_email_message(payload.message)
#     return obj
@router.post("/", response_model=ChatMessageListItem)
def chat_create_message(
    payload: ChatMessagePayload,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session)
):
    data = payload.model_dump()
    obj = ChatMessage.model_validate(data)
    obj.status = "pending"
    session.add(obj)
    session.commit()
    session.refresh(obj)
    background_tasks.add_task(process_ai_response, obj.id, obj.message)
    return obj
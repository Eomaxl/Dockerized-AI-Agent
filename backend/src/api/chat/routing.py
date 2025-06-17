from fastapi import APIRouter

router = APIRouter()

# /api/chats/
@router.get("/")
def chat_health():
    return {"status":"ok"}
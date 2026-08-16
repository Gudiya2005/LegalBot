from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.dependencies import get_db

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import generate_reply
from app.services.chat_history_service import (
    get_recent_conversations,
    get_chat_history
)

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


@router.post("/", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    result = generate_reply(
        db=db,
        email=current_user,
        message=request.message,
        conversation_id=request.conversation_id,
        tool=request.tool
    )

    return ChatResponse(
        intent=result["intent"],
        reply=result["reply"],
        language=result["language"],
        emergency=result["emergency"],
        is_new_incident=result["is_new_incident"],
        complaint_requested=result["complaint_requested"],
        missing_information=result[
            "missing_information"
        ],
        information_complete=result[
            "information_complete"
        ],
        sources=result["sources"],
        generated_document=result[
            "generated_document"
        ]
    )

@router.get("/history")
def chat_history(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    from app.services.user_service import get_user_by_email

    user = get_user_by_email(
        db,
        current_user
    )

    if not user:
        return []

    conversations = get_recent_conversations(
        db=db,
        user_id=user.id,
        limit=10
    )

    return conversations

@router.get("/history/{conversation_id}")
def conversation_history(
    conversation_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    from app.services.user_service import get_user_by_email

    user = get_user_by_email(
        db,
        current_user
    )

    if not user:
        return []

    chats = get_chat_history(
        db=db,
        user_id=user.id,
        conversation_id=conversation_id,
        limit=100
    )

    return [
        {
            "role": chat.role,
            "message": chat.message,
            "tool": chat.tool or "main",
            "created_at": chat.created_at
        }
        for chat in chats
    ]
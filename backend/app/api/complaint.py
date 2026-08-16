from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.dependencies import get_db

from app.orchestrator.agent_context import AgentContext
from app.orchestrator.complaint_manager import ComplaintManager


router = APIRouter(
    prefix="/complaint",
    tags=["complaint"]
)

manager = ComplaintManager()


@router.post("/")
def complaint(
    request: dict,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    message = request.get("message", "")
    history = request.get("history", [])

    context = AgentContext(
        user_id=0,
        message=message
    )

    context.chat_history = history

    result = manager.run(context)

    return {
        "intent": result.intent,
        "reply": result.final_response,
        "complaint_requested": result.complaint_requested,
        "complaint_ready": result.complaint_ready,
        "generated_document": result.generated_document or "",
        "sources": result.knowledge_sources
    }
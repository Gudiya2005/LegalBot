from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.dependencies import get_db

from app.orchestrator.agent_context import AgentContext
from app.orchestrator.evidence_manager import EvidenceManager


router = APIRouter(
    prefix="/evidence",
    tags=["evidence"]
)

manager = EvidenceManager()


@router.post("/")
def evidence(
    request: dict,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    message = request.get("message", "")
    history = request.get("history", [])

    context = AgentContext(
        user_id=0,
        message=message,
        tool="evidence"
    )

    context.chat_history = history
    context.retrieved_knowledge = ""

    result = manager.run(context)

    return {
        "intent": result.intent,
        "reply": result.final_response,
        "evidence": result.evidence_checklist,
        "sources": result.knowledge_sources
    }
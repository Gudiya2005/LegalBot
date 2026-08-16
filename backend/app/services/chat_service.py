from sqlalchemy.orm import Session

from app.orchestrator.agent_context import AgentContext
from app.orchestrator.agent_manager import AgentManager
from app.orchestrator.scam_manager import ScamManager

from app.services.chat_history_service import (
    save_message,
    get_chat_history,
    format_chat_history
)

from app.services.user_service import get_user_by_email


manager = AgentManager()
scam_manager = ScamManager()

def generate_reply(
    db: Session,
    email: str,
    message: str,
    conversation_id: str,
    tool: str = "main"
):

    # -----------------------------------
    # 1. Get user
    # -----------------------------------

    user = get_user_by_email(db, email)

    if not user:
        raise Exception("User not found")


    # -----------------------------------
    # 2. Get previous chat history
    # -----------------------------------

    history = get_chat_history(
        db,
        user.id,
        conversation_id
    )

    print("\n========== PREVIOUS HISTORY ==========")

    for chat in history:
        print(
            f"{chat.role}: {chat.message}"
        )

    print("======================================\n")


    # -----------------------------------
    # 3. Create Agent Context
    # -----------------------------------

    context = AgentContext(
        user_id=user.id,
        message=message,
        tool=tool
    )


    # -----------------------------------
    # 4. Pass previous conversation
    # -----------------------------------

    context.chat_history = [
        {
            "role": chat.role,
            "message": chat.message
        }
        for chat in history
    ]


    # -----------------------------------
    # 5. Run Agent Pipeline
    # -----------------------------------

    if tool == "scam":
        result = scam_manager.run(context)
    else:
        result = manager.run(context)


    # -----------------------------------
    # 6. Save user message
    # -----------------------------------

    save_message(
        db,
        user.id,
        conversation_id,
        "user",
        message,
        tool
    )


    # -----------------------------------
    # 7. Save assistant response
    # -----------------------------------

    save_message(
        db,
        user.id,
        conversation_id,
        "assistant",
        result.final_response,
        tool
    )


    # -----------------------------------
    # 8. Return structured result
    # -----------------------------------

    return {
        "intent": result.intent,

        "language": result.language,

        "emergency": result.emergency,

        "is_new_incident":
            result.is_new_incident,

        "complaint_requested":
            result.complaint_requested,

        "reply":
            result.final_response,

        "sources":
            result.knowledge_sources,

        "missing_information":
            result.missing_information,

        "information_complete":
            result.information_complete,

        "generated_document":
            result.generated_document or ""
    }
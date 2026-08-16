from sqlalchemy.orm import Session

from app.models.chat import ChatHistory


def save_message(
    db: Session,
    user_id: int,
    conversation_id: str,
    role: str,
    message: str,
    tool: str = "main"
):
    chat = ChatHistory(
        user_id=user_id,
        conversation_id=conversation_id,
        role=role,
        message=message,
        tool=tool
    )

    db.add(chat)
    db.commit()
    db.refresh(chat)

    return chat


def get_chat_history(
    db: Session,
    user_id: int,
    conversation_id: str,
    limit: int = 10
):
    chats = (
        db.query(ChatHistory)
        .filter(
            ChatHistory.user_id == user_id,
            ChatHistory.conversation_id == conversation_id
        )
        .order_by(ChatHistory.id.desc())
        .limit(limit)
        .all()
    )

    return chats[::-1]


def format_chat_history(chats):
    history = ""

    for chat in chats:
        history += f"{chat.role}: {chat.message}\n"

    return history


def get_recent_conversations(
    db: Session,
    user_id: int,
    limit: int = 10
):
    chats = (
        db.query(ChatHistory)
        .filter(
            ChatHistory.user_id == user_id
        )
        .order_by(ChatHistory.id.desc())
        .all()
    )

    conversations = {}

    for chat in chats:

        conversation_id = chat.conversation_id

        if conversation_id not in conversations:

            # Find the first user message for this conversation
            user_message = None

            for previous_chat in reversed(chats):

                if (
                    previous_chat.conversation_id
                    == conversation_id
                    and previous_chat.role == "user"
                ):
                    user_message = previous_chat.message
                    break

            if not user_message:
                user_message = "New Chat"

            # Clean title
            title = " ".join(
                user_message.strip().split()
            )

            # Keep sidebar title short
            if len(title) > 45:
                title = title[:45].rstrip() + "..."

            conversations[conversation_id] = {
                "conversation_id": conversation_id,
                "title": title,
                "updated_at": chat.created_at
            }

    return list(conversations.values())[:limit]
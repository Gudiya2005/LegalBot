from app.models.user import User
from app.models.chat import ChatHistory

from app.database.database import SessionLocal
from app.services.chat_history_service import (
    save_message,
    get_chat_history
)

db = SessionLocal()

# Save a user message
save_message(
    db=db,
    user_id=1,
    role="user",
    message="My Instagram account was hacked."
)

# Save an assistant message
save_message(
    db=db,
    user_id=1,
    role="assistant",
    message="Please reset your password immediately."
)

# Fetch history
history = get_chat_history(db, user_id=1)

print("=" * 50)

for chat in history:
    print(chat.role)
    print(chat.message)
    print("-" * 30)

db.close()
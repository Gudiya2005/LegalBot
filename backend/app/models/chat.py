from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.database.database import Base


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    conversation_id = Column(Text, index=True, nullable=False)

    role = Column(Text)

    message = Column(Text)

    tool = Column(Text, default="main")

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
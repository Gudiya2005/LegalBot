from app.database.database import SessionLocal
from app.models.chat import ChatHistory

db = SessionLocal()

db.query(ChatHistory).delete()

db.commit()
db.close()

print("Chat history cleared.")
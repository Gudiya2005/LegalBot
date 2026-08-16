from app.database.database import SessionLocal
from app.services.chat_service import generate_reply


db = SessionLocal()

email = "gudiya4@gmail.com"

try:

    result = generate_reply(
        db=db,
        email=email,
        message="My Instagram account was hacked. I cannot access it anymore. It happened today."    )

    print("\n===== RESPONSE =====")
    print(result)

finally:
    db.close()
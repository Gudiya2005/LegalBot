from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database.database import engine, Base
from app.models.user import User
from app.models.chat import ChatHistory

from app.api.auth import router as auth_router
from app.api.chat import router as chat_router

from app.api.complaint import router as complaint_router
from app.api.emergency import router as emergency_router
from app.api.evidence import router as evidence_router

# =========================
# VOICE ASSISTANT
# =========================

from app.api.voice import router as voice_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


# Allow React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# API ROUTERS
# =========================

app.include_router(auth_router)

app.include_router(chat_router)

app.include_router(complaint_router)

app.include_router(emergency_router)

app.include_router(evidence_router)

# Voice / Whisper
app.include_router(voice_router)


@app.get("/")
def home():
    return {
        "message": f"Welcome to {settings.APP_NAME}"
    }

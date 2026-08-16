from pydantic import BaseModel

class ChatRequest(BaseModel):

    message: str
    conversation_id: str
    tool: str = "main"

class ChatResponse(BaseModel):

    intent: str

    reply: str

    language: str

    emergency: bool

    is_new_incident: bool

    complaint_requested: bool

    missing_information: list

    information_complete: bool

    sources: list

    generated_document: str
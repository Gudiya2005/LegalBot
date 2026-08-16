import google.generativeai as genai

from app.config import settings
from app.prompts.system_prompt import SYSTEM_PROMPT

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def ask_gemini(user_message: str, knowledge: str, history: str):
    prompt = f"""
{SYSTEM_PROMPT}

Previous Conversation:
{history if history else "No previous conversation."}

Knowledge Base:
{knowledge if knowledge else "No specific knowledge found."}

Current User Question:
{user_message}
"""

    response = model.generate_content(prompt)

    return response.text
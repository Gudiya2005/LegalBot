from langdetect import detect, LangDetectException

from app.agents.base_agent import BaseAgent

class LanguageAgent(BaseAgent):
    def __init__(self):
        super().__init__("Language Agent")

    def execute(self, context):
        try:
            context.language = detect(context.message)
        except LangDetectException:
            context.language = "unknown"

        return context
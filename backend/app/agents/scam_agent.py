from app.agents.base_agent import BaseAgent


class ScamAgent(BaseAgent):

    def __init__(self):
        super().__init__("Scam Checker")

    def execute(self, context):

        # Scam analysis is handled by Gemini.
        # This agent marks the response as scam-analysis mode.
        context.response_plan["scam_check"] = True

        return context
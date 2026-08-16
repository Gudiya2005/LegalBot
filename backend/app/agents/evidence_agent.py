from app.agents.base_agent import BaseAgent


class EvidenceAgent(BaseAgent):

    def __init__(self):
        super().__init__("Evidence Guide")

    def execute(self, context):

        # Gemini already provides incident-specific
        # evidence. Preserve it if available.

        existing = context.evidence_checklist or []

        # Generic fallback only when Gemini did not
        # provide evidence.
        if not existing:

            existing = [
                "Keep relevant screenshots",
                "Preserve emails, messages, and communication records",
                "Do not delete potentially relevant evidence"
            ]

        # Remove duplicates
        context.evidence_checklist = list(
            dict.fromkeys(existing)
        )

        return context
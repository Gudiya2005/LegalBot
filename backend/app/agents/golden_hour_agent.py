from app.agents.base_agent import BaseAgent


class GoldenHourAgent(BaseAgent):

    def __init__(self):
        super().__init__("Golden Hour Wizard")

    def execute(self, context):

        if not context.emergency:
            return context

        # Gemini has already generated immediate actions.
        # Preserve them.

        context.response_plan[
            "show_golden_hour"
        ] = True

        return context
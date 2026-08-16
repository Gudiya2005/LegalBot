from app.agents.base_agent import BaseAgent


class EmergencyAgent(BaseAgent):

    def __init__(self):
        super().__init__("Emergency Agent")

    def execute(self, context):

        if not context.emergency:
            return context

        print(
            "🚨 Emergency situation detected."
        )

        # Gemini already provides immediate actions.
        # Do not ask additional questions here.

        if context.golden_hour_actions:

            context.response_plan[
                "emergency"
            ] = True

            context.response_plan[
                "priority"
            ] = "immediate"

        return context
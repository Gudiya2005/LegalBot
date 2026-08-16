from app.agents.base_agent import BaseAgent

class ResponsePlannerAgent(BaseAgent):

    def __init__(self):
        super().__init__("Response Planner")

    def execute(self, context):

        context.response_plan = {
            "show_golden_hour": context.emergency,
            "ask_questions": not context.information_complete,
            "show_evidence": True,
            "use_rag": True,
            "generate_document": True,
        }

        return context
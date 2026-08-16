from app.orchestrator.agent_context import AgentContext

from app.agents.gemini_brain_agent import GeminiBrainAgent
from app.agents.complaint_agent import ComplaintAgent
from app.agents.response_formatter_agent import ResponseFormatterAgent


class ComplaintManager:

    def __init__(self):

        self.agents = [
            GeminiBrainAgent(),
            ComplaintAgent(),
            ResponseFormatterAgent()
        ]

    def run(self, context: AgentContext):

        for agent in self.agents:

            print(
                f"▶ Running Complaint Agent: {agent.name}"
            )

            context = agent.execute(context)

        return context
from app.orchestrator.agent_context import AgentContext

from app.agents.gemini_brain_agent import GeminiBrainAgent
from app.agents.scam_agent import ScamAgent
from app.agents.response_formatter_agent import ResponseFormatterAgent


class ScamManager:

    def __init__(self):

        self.agents = [
            GeminiBrainAgent(),
            ScamAgent(),
            ResponseFormatterAgent()
        ]

    def run(self, context: AgentContext):

        for agent in self.agents:

            print(
                f"▶ Running Scam Agent: {agent.name}"
            )

            context = agent.execute(context)

        return context
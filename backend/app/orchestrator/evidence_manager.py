from app.orchestrator.agent_context import AgentContext

from app.agents.gemini_brain_agent import GeminiBrainAgent
from app.agents.evidence_agent import EvidenceAgent
from app.agents.response_formatter_agent import ResponseFormatterAgent


class EvidenceManager:

    def __init__(self):

        self.agents = [
            GeminiBrainAgent(),
            EvidenceAgent(),
            ResponseFormatterAgent()
        ]

    def run(self, context: AgentContext):

        for agent in self.agents:

            print(
                f"▶ Running Evidence Agent: {agent.name}"
            )

            context = agent.execute(context)

        return context
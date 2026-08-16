from app.orchestrator.agent_context import AgentContext

from app.agents.gemini_brain_agent import GeminiBrainAgent
from app.agents.emergency_agent import EmergencyAgent
from app.agents.response_formatter_agent import ResponseFormatterAgent


class EmergencyManager:

    def __init__(self):

        self.agents = [
            GeminiBrainAgent(),
            EmergencyAgent(),
            ResponseFormatterAgent()
        ]

    def run(self, context: AgentContext):

        for agent in self.agents:

            print(
                f"▶ Running Emergency Agent: {agent.name}"
            )

            context = agent.execute(context)

        return context
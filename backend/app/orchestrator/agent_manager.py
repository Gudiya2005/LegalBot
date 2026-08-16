from app.orchestrator.agent_context import AgentContext

from app.agents.gemini_brain_agent import GeminiBrainAgent
from app.agents.emergency_agent import EmergencyAgent
from app.agents.golden_hour_agent import GoldenHourAgent
from app.agents.rag_retrieval_agent import RAGRetrievalAgent
from app.agents.evidence_agent import EvidenceAgent
from app.agents.complaint_agent import ComplaintAgent
from app.agents.response_formatter_agent import ResponseFormatterAgent


class AgentManager:

    def __init__(self):

        self.agents = [
            GeminiBrainAgent(),
            EmergencyAgent(),
            GoldenHourAgent(),
            RAGRetrievalAgent(),
            EvidenceAgent(),
            ComplaintAgent(),
            ResponseFormatterAgent()
        ]

    def run(self, context: AgentContext):

        for agent in self.agents:

            print(
                f"▶ Running Agent: {agent.name}"
            )

            context = agent.execute(context)

        return context
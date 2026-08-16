from app.agents.base_agent import BaseAgent
from app.rag.retriever import retrieve_knowledge


class RAGRetrievalAgent(BaseAgent):

    def __init__(self):
        super().__init__("RAG Retrieval Agent")

    def execute(self, context):

        knowledge, sources = retrieve_knowledge(
            context.message,
            context.intent
        )

        context.retrieved_knowledge = knowledge
        context.knowledge_sources = sources

        return context
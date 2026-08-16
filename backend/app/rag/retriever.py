from pathlib import Path

from app.rag.vector_store import vector_store


def retrieve_knowledge(query: str, intent: str = None, k: int = 3):

    search_kwargs = {}

    if intent:
        source_path = str(
            Path(__file__).resolve().parents[2]
            / "knowledge_base"
            / f"{intent}.md"
        )

        search_kwargs["filter"] = {
            "source": source_path
        }

    results = vector_store.similarity_search(
        query,
        k=k,
        **search_kwargs
    )

    unique_content = []
    sources = []

    for doc in results:

        content = doc.page_content.strip()

        if content and content not in unique_content:
            unique_content.append(content)

        source = doc.metadata.get("source", "Unknown")

        if source not in sources:
            sources.append(source)

    knowledge = "\n\n".join(unique_content)

    return knowledge, sources
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader


BASE_DIR = Path(__file__).resolve().parents[2]
KNOWLEDGE_DIR = BASE_DIR / "knowledge_base"


def load_documents():

    loader = DirectoryLoader(
        path=str(KNOWLEDGE_DIR),
        glob="*.md",
        loader_cls=TextLoader
    )

    documents = loader.load()

    for document in documents:
        source = Path(document.metadata["source"]).stem
        document.metadata["category"] = source

    return documents
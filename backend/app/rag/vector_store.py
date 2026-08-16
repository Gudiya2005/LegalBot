from pathlib import Path

from langchain_chroma import Chroma

from app.rag.embeddings import get_embeddings

BASE_DIR = Path(__file__).resolve().parents[2]
VECTOR_DB_DIR = BASE_DIR / "vector_db"

# Load the embedding model once
embedding_model = get_embeddings()

# Load the existing Chroma database
vector_store = Chroma(
    persist_directory=str(VECTOR_DB_DIR),
    embedding_function=embedding_model
)
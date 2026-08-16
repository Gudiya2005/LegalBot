from app.rag.embeddings import get_embeddings

embedding_model = get_embeddings()

vector = embedding_model.embed_query(
    "My Instagram account was hacked."
)

print(f"Vector Length : {len(vector)}")

print(vector[:10])
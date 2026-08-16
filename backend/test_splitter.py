from app.rag.loader import load_documents
from app.rag.splitter import split_document

docs = load_documents()
chunks = split_document(docs)

print(f"Documents : {len(docs)}")
print(f"Chunks : {len(chunks)}")

for i, chunk in enumerate(chunks, start=1):
    print("=" * 50)
    print(f"chunk {i}")
    print(chunk.metadata)
    print(chunk.page_content[:300])
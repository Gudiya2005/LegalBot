from app.rag.loader import load_documents

docs = load_documents()

print(f"Total Documents:{len(docs)}")

for doc in docs:
    print("=" *40)
    print(doc.metadata)
    print(doc.page_content[:200])
from app.rag.vector_store import create_vector_store

db = create_vector_store()

print("Vector database created successfully!")

print(f"Total Chunks Stored: {db._collection.count()}")
from app.rag.retriever import retrieve_knowledge

question = "Someone pretending to be a police officer is asking me to transfer money."

knowledge = retrieve_knowledge(question)

print("=" * 50)
print(knowledge)

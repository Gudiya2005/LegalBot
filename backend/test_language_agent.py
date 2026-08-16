from app.orchestrator.agent_context import AgentContext
from app.orchestrator.agent_manager import AgentManager


manager = AgentManager()

context = AgentContext(
    user_id=1,
    message="Instagram. I can't access it. It happened today."
)

# Simulate user selecting a document
context.selected_document = "police_complaint"

result = manager.run(context)

print("Language:", result.language)
print("Intent:", result.intent)
print("Emergency:", result.emergency)
print("Missing Information:", result.missing_information)
print("Information Complete:", result.information_complete)

print("\nEvidence:")
for item in result.evidence_checklist:
    print(f"- {item}")

print("\nKnowledge:")
print(result.retrieved_knowledge)

print("\nSources:")
for source in result.knowledge_sources:
    print(f"- {source}")

print("\nResponse Plan:")
print(result.response_plan)

print("\nGenerated Document:")
print(result.generated_document)

print("\n================ FINAL RESPONSE ================\n")
print(result.final_response)

print("Collected Information:", result.collected_information)
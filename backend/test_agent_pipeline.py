from app.orchestrator.agent_context import AgentContext
from app.orchestrator.agent_manager import AgentManager


manager = AgentManager()


context = AgentContext(
    user_id=1,
    message="Someone called me pretending to be a police officer and demanded money."
)

context.chat_history = []


result = manager.run(context)


print("\n")
print("=" * 60)
print("FINAL RESULT")
print("=" * 60)

print("\nLanguage:")
print(result.language)

print("\nIncident:")
print(result.intent)

print("\nEmergency:")
print(result.emergency)

print("\nMissing Information:")
print(result.missing_information)

print("\nEvidence:")
print(result.evidence_checklist)

print("\nImmediate Actions:")
print(result.golden_hour_actions)

print("\nFinal Response:")
print(result.final_response)

print("\n")
from app.orchestrator.agent_context import AgentContext
from app.agents.complaint_agent import ComplaintAgent


agent = ComplaintAgent()


# -----------------------------------------
# TEST 1: Complaint NOT requested
# -----------------------------------------

context = AgentContext(
    user_id=1,
    message="My Instagram account was hacked."
)

context.intent = "Social Media Account Hacking"

context.collected_information = {
    "platform": "Instagram",
    "account_access": "No",
    "incident_date": "Today"
}

context.evidence_checklist = [
    "Login alerts",
    "Recovery emails",
    "Screenshots"
]

context.information_complete = True

context.complaint_requested = False


result = agent.execute(context)


print("\n========== TEST 1 ==========")
print("Complaint requested:", result.complaint_requested)
print("Generated document:")
print(repr(result.generated_document))


# -----------------------------------------
# TEST 2: Complaint requested
# -----------------------------------------

context = AgentContext(
    user_id=1,
    message="Please draft a complaint for me."
)

context.intent = "Social Media Account Hacking"

context.collected_information = {
    "platform": "Instagram",
    "account_access": "No",
    "incident_date": "Today"
}

context.evidence_checklist = [
    "Login alerts",
    "Recovery emails",
    "Screenshots"
]

context.information_complete = True
context.complaint_requested = True
context.complaint_ready = True

result = agent.execute(context)


print("\n========== TEST 2 ==========")
print("Complaint requested:", result.complaint_requested)
print("Complaint ready:", result.complaint_ready)
print("\nGenerated document:")
print(result.generated_document)

# -----------------------------------------
# TEST 3: UPI Fraud Complaint
# -----------------------------------------

context = AgentContext(
    user_id=1,
    message="Someone made an unauthorized UPI transaction."
)

context.incident_type = "UPI Fraud"

context.collected_information = {
    "payment_app": "Google Pay",
    "amount_lost": "₹8,500",
    "transaction_date": "Today",
    "incident_description": (
        "Someone made an unauthorized UPI transaction "
        "of ₹8,500 from my Google Pay account."
    )
}

context.information_complete = True

context.complaint_requested = True
context.complaint_ready = True

result = agent.execute(context)

print("\n========== TEST 3 ==========")
print("Complaint requested:", result.complaint_requested)
print("Complaint ready:", result.complaint_ready)
print("\nGenerated document:")
print(result.generated_document)

# -----------------------------------------
# TEST 4: OTP Fraud Complaint
# -----------------------------------------

context = AgentContext(
    user_id=1,
    message="Someone called me pretending to be my bank and asked for an OTP."
)

context.incident_type = "OTP Fraud"

context.collected_information = {
    "otp_shared": "Yes",
    "money_deducted": "No",
    "incident_description": (
        "Someone called me pretending to be my bank and asked "
        "me for an OTP."
    )
}

context.information_complete = True

context.complaint_requested = True
context.complaint_ready = True

result = agent.execute(context)

print("\n========== TEST 4 ==========")
print("Complaint requested:", result.complaint_requested)
print("Complaint ready:", result.complaint_ready)
print("\nGenerated document:")
print(result.generated_document)
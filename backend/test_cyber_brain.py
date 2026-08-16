from app.services.cyber_brain_service import ask_cyber_brain


tests = [
    "My Instagram account was hacked.",

    "Someone made an unauthorized UPI transaction from my bank account.",

    "I clicked a suspicious link and entered my bank details.",

    "Someone called me pretending to be a police officer and demanded money.",

    "I just transferred 50000 rupees to a scammer through UPI.",

    "Someone is using my Aadhaar details without my permission.",

    "My email account was compromised and the recovery email was changed.",

    "How can I protect myself from online scams?"
]


for i, message in enumerate(tests, start=1):

    print("\n")
    print("=" * 70)
    print(f"TEST {i}")
    print("=" * 70)

    print("\nUSER:")
    print(message)

    result = ask_cyber_brain(
        message=message,
        history=[],
        knowledge=""
    )

    print("\nGEMINI RESULT:")

    print("Language:", result.get("language"))
    print("Cyber Related:", result.get("is_cyber_related"))
    print("New Incident:", result.get("is_new_incident"))
    print("Incident Type:", result.get("incident_type"))
    print("General Query:", result.get("is_general_query"))
    print("Emergency:", result.get("is_emergency"))

    print("\nMissing Information:")
    for item in result.get("missing_information", []):
        print("-", item)

    print("\nCollected Information:")
    print(result.get("collected_information"))

    print("\nEvidence:")
    for item in result.get("evidence", []):
        print("-", item)

    print("\nImmediate Actions:")
    for item in result.get("immediate_actions", []):
        print("-", item)

    print("\nComplaint Requested:")
    print(result.get("complaint_requested"))

    print("\nComplaint Ready:")
    print(result.get("complaint_ready"))

    print("\nResponse:")
    print(result.get("response"))

    print("\n")
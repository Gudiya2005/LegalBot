from app.services.cyber_brain_service import ask_cyber_brain


print("\n================ REAL CONVERSATION TEST ================\n")


history = []


# =========================================================
# MESSAGE 1
# =========================================================

message_1 = "My Instagram account was hacked."

result_1 = ask_cyber_brain(
    message=message_1,
    history=history,
    knowledge=""
)

print("\n================ MESSAGE 1 ================\n")

print("USER:")
print(message_1)

print("\nGEMINI:")
print(result_1.get("response"))

print("\nIncident:")
print(result_1.get("incident_type"))

print("\nCollected Information:")
print(result_1.get("collected_information"))

print("\nMissing Information:")
print(result_1.get("missing_information"))

print("\nComplaint Requested:")
print(result_1.get("complaint_requested"))


# =========================================================
# SAVE MESSAGE 1 TO HISTORY
# =========================================================

history.append({
    "role": "user",
    "message": message_1
})

history.append({
    "role": "assistant",
    "message": result_1.get("response", "")
})


# =========================================================
# MESSAGE 2
# =========================================================

message_2 = "I cannot access it and it happened today."

result_2 = ask_cyber_brain(
    message=message_2,
    history=history,
    knowledge=""
)

print("\n================ MESSAGE 2 ================\n")

print("USER:")
print(message_2)

print("\nGEMINI:")
print(result_2.get("response"))

print("\nIncident:")
print(result_2.get("incident_type"))

print("\nCollected Information:")
print(result_2.get("collected_information"))

print("\nMissing Information:")
print(result_2.get("missing_information"))

print("\nComplaint Requested:")
print(result_2.get("complaint_requested"))


# =========================================================
# SAVE MESSAGE 2 TO HISTORY
# =========================================================

history.append({
    "role": "user",
    "message": message_2
})

history.append({
    "role": "assistant",
    "message": result_2.get("response", "")
})


# =========================================================
# MESSAGE 3
# =========================================================

message_3 = "Please draft a complaint for me."

result_3 = ask_cyber_brain(
    message=message_3,
    history=history,
    knowledge=""
)

print("\n================ MESSAGE 3 ================\n")

print("USER:")
print(message_3)

print("\nGEMINI:")
print(result_3.get("response"))

print("\nIncident:")
print(result_3.get("incident_type"))

print("\nCollected Information:")
print(result_3.get("collected_information"))

print("\nMissing Information:")
print(result_3.get("missing_information"))

print("\nComplaint Requested:")
print(result_3.get("complaint_requested"))

print("\nComplaint Ready:")
print(result_3.get("complaint_ready"))


print("\n================ FINAL HISTORY ================\n")

for item in history:
    print(
        f"{item['role']}: {item['message']}"
    )

print("\n================================================\n")
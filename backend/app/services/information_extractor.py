import json
import re

from google import genai

from app.config import settings


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


# ============================================================
# FALLBACK INFORMATION EXTRACTION
# ============================================================

def fallback_extract(
    message: str,
    intent: str,
    previous_information: dict
):

    text = message.lower().strip()

    information = previous_information.copy()


    # --------------------------------------------------------
    # SOCIAL MEDIA HACKING
    # --------------------------------------------------------

    if intent == "social_media_hacking":

        # Platform
        platforms = {
            "instagram": "Instagram",
            "facebook": "Facebook",
            "whatsapp": "WhatsApp",
            "twitter": "Twitter",
            "x": "X",
            "linkedin": "LinkedIn",
            "snapchat": "Snapchat",
            "telegram": "Telegram"
        }

        for keyword, platform in platforms.items():

            if re.search(
                rf"\b{re.escape(keyword)}\b",
                text
            ):

                information["platform"] = platform
                break


        # Account access
        no_access_phrases = [
            "cannot access",
            "can't access",
            "cant access",
            "unable to access",
            "cannot login",
            "can't login",
            "cant login",
            "unable to login",
            "cannot log in",
            "can't log in",
            "cant log in",
            "unable to log in",
            "lost access",
            "no access"
        ]

        yes_access_phrases = [
            "i can access",
            "i still have access",
            "still have access",
            "i can login",
            "i can log in",
            "i still can access"
        ]


        if any(
            phrase in text
            for phrase in no_access_phrases
        ):

            information["account_access"] = "No"


        elif any(
            phrase in text
            for phrase in yes_access_phrases
        ):

            information["account_access"] = "Yes"


        # Incident date
        if "today" in text:

            information["incident_date"] = "Today"

        elif "yesterday" in text:

            information["incident_date"] = "Yesterday"

        elif "last night" in text:

            information["incident_date"] = "Last night"

        elif "this morning" in text:

            information["incident_date"] = "Today"


    # --------------------------------------------------------
    # UPI FRAUD
    # --------------------------------------------------------

    elif intent == "upi_fraud":

        apps = {
            "gpay": "Google Pay",
            "google pay": "Google Pay",
            "phonepe": "PhonePe",
            "paytm": "Paytm",
            "upi": "UPI"
        }

        for keyword, app_name in apps.items():

            if keyword in text:

                information["payment_app"] = app_name
                break


        # Amount
        amount_match = re.search(
            r"(?:₹|rs\.?|inr)\s?([\d,]+(?:\.\d+)?)",
            text
        )

        if amount_match:

            information["amount_lost"] = (
                "₹" + amount_match.group(1)
            )


        if "today" in text:

            information["transaction_date"] = "Today"

        elif "yesterday" in text:

            information["transaction_date"] = "Yesterday"


    # --------------------------------------------------------
    # OTP FRAUD
    # --------------------------------------------------------

    elif intent == "otp_fraud":

        if any(
            phrase in text
            for phrase in [
                "shared otp",
                "shared the otp",
                "gave otp",
                "gave the otp",
                "yes i shared",
                "yes, i shared"
            ]
        ):

            information["otp_shared"] = "Yes"


        elif any(
            phrase in text
            for phrase in [
                "did not share",
                "didn't share",
                "didnt share",
                "not shared"
            ]
        ):

            information["otp_shared"] = "No"


        if any(
            phrase in text
            for phrase in [
                "money deducted",
                "money was deducted",
                "amount deducted",
                "money debited",
                "amount debited"
            ]
        ):

            information["money_deducted"] = "Yes"


        elif any(
            phrase in text
            for phrase in [
                "no money deducted",
                "money was not deducted",
                "nothing deducted",
                "no amount deducted"
            ]
        ):

            information["money_deducted"] = "No"


    return information


# ============================================================
# MAIN INFORMATION EXTRACTION
# ============================================================

def extract_information(
    message: str,
    intent: str,
    missing_information: list[str],
    previous_information: dict,
    chat_history: list
):

    prompt = f"""
You are the information extraction component of a cyber crime assistant.

Your job is to maintain a COMPLETE set of incident information across
multiple messages in a conversation.

Cyber crime type:
{intent}

Previous conversation:
{json.dumps(chat_history, ensure_ascii=False)}

Previously collected information:
{json.dumps(previous_information, ensure_ascii=False)}

Information still required:
{json.dumps(missing_information, ensure_ascii=False)}

Current user message:
{message}

IMPORTANT RULES:

1. Use BOTH the previous conversation and the current user message.

2. Do NOT treat the current message as a completely new incident.

3. Preserve previously collected information.

4. Add newly provided information.

5. Never remove previously collected information unless the user clearly
   corrects or changes it.

6. Resolve references such as:
   "it",
   "my account",
   "that account"
   using the previous conversation.

7. Do not invent information.

8. Only extract information relevant to the current cyber crime type.

9. Return the COMPLETE collected information.

10. Use ONLY these field names:

- platform
- account_access
- incident_date
- payment_app
- amount_lost
- transaction_date
- otp_shared
- money_deducted

If a field is unknown, do not include it.

Example:

Previous user message:
"My Instagram account was hacked."

Current user message:
"I cannot access it and it happened today."

Previously collected information:
{{
    "platform": "Instagram"
}}

Correct output:

{{
    "platform": "Instagram",
    "account_access": "No",
    "incident_date": "Today"
}}

Return ONLY valid JSON.
Do not use Markdown.
Do not add explanations.
"""


    # ========================================================
    # TRY GEMINI
    # ========================================================

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        raw_response = response.text.strip()


        print(
            "\n===== INFORMATION EXTRACTION ====="
        )

        print(raw_response)

        print(
            "==================================\n"
        )


        # Remove Markdown fences

        if raw_response.startswith("```"):

            raw_response = raw_response.replace(
                "```json",
                ""
            )

            raw_response = raw_response.replace(
                "```",
                ""
            )

            raw_response = raw_response.strip()


        extracted = json.loads(
            raw_response
        )


        if not isinstance(
            extracted,
            dict
        ):

            return previous_information.copy()


        allowed_fields = {
            "platform",
            "account_access",
            "incident_date",
            "payment_app",
            "amount_lost",
            "transaction_date",
            "otp_shared",
            "money_deducted"
        }


        cleaned_information = {

            key: value

            for key, value in extracted.items()

            if key in allowed_fields
        }


        complete_information = (
            previous_information.copy()
        )

        complete_information.update(
            cleaned_information
        )


        return complete_information


    # ========================================================
    # GEMINI FAILED
    # ========================================================

    except Exception as error:

        print(
            "\n⚠️ Gemini information extraction failed."
        )

        print(
            f"Reason: {error}"
        )

        print(
            "Using local fallback extraction."
        )


        return fallback_extract(
            message=message,
            intent=intent,
            previous_information=previous_information
        )
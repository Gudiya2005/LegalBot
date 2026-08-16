from app.agents.base_agent import BaseAgent


class ComplaintAgent(BaseAgent):

    def __init__(self):
        super().__init__("Complaint Generator")

    def execute(self, context):

        # Never generate a complaint unless the user explicitly requested it.
        if not context.complaint_requested:
            context.complaint_ready = False
            context.generated_document = ""
            return context

        # If Gemini says more essential information is needed,
        # let the conversation continue instead of generating a weak draft.
        if not context.complaint_ready:
            context.generated_document = ""
            return context

        info = context.collected_information or {}

        platform = info.get("platform", "")
        account_access = info.get("account_access", "")
        incident_date = info.get("incident_date", "")
        suspicious_activity = info.get("suspicious_activity", "")

        payment_app = info.get("payment_app", "")
        amount_lost = info.get("amount_lost", "")
        transaction_date = info.get("transaction_date", "")

        otp_shared = info.get("otp_shared", "")
        money_deducted = info.get("money_deducted", "")

        caller_identity = info.get("caller_identity", "")
        caller_phone = info.get("caller_phone", "")
        money_transferred = info.get("money_transferred", "")

        personal_information_shared = info.get(
            "personal_information_shared", ""
        )

        incident_description = info.get(
            "incident_description", ""
        )

        incident_type = (
            context.incident_type
            or context.intent
            or "Cyber Crime"
        ).strip()

        # ---------------------------------------------------------
        # Determine a useful description from collected facts.
        # ---------------------------------------------------------

        description = incident_description.strip()

        if not description:
            if "social media" in incident_type.lower() or "account hacking" in incident_type.lower():
                description = (
                    f"My {platform or 'social media'} account was hacked "
                    "and I believe an unauthorized person gained access to it."
                )

            elif "upi" in incident_type.lower() or "financial" in incident_type.lower():
                description = (
                    "I noticed an unauthorized transaction from my account "
                    "which I did not initiate or authorize."
                )

            elif "otp" in incident_type.lower():
                description = (
                    "I received a suspicious call/message requesting an OTP "
                    "in connection with my account."
                )

            elif (
                "police impersonation" in incident_type.lower()
                or "digital arrest" in incident_type.lower()
            ):
                description = (
                    "I was contacted by a person who falsely claimed to be "
                    f"{caller_identity or 'a police officer'} and attempted "
                    "to obtain money or personal information from me."
                )

            elif "phishing" in incident_type.lower():
                description = (
                    "I was directed to a suspicious website/link and was "
                    "asked to provide personal or financial information."
                )

            elif "identity theft" in incident_type.lower() or "aadhaar" in incident_type.lower():
                description = (
                    "I believe my identity information has been used "
                    "without my permission."
                )

            else:
                description = (
                    "I would like to report the cyber crime incident "
                    "described above."
                )

        # ---------------------------------------------------------
        # Subject
        # ---------------------------------------------------------

        if platform:
            subject = (
                f"Complaint Regarding Hacking and Unauthorized Access "
                f"to My {platform} Account"
            )
        elif "upi" in incident_type.lower():
            subject = "Complaint Regarding Unauthorized UPI Transaction"
        elif "otp" in incident_type.lower():
            subject = "Complaint Regarding OTP Fraud"
        elif (
            "police impersonation" in incident_type.lower()
            or "digital arrest" in incident_type.lower()
        ):
            subject = "Complaint Regarding Police Impersonation / Online Fraud"
        elif "phishing" in incident_type.lower():
            subject = "Complaint Regarding Phishing and Unauthorized Use of Information"
        elif "identity theft" in incident_type.lower():
            subject = "Complaint Regarding Identity Theft / Unauthorized Use of Personal Information"
        else:
            subject = f"Complaint Regarding {incident_type}"

        lines = [
            "CYBER CRIME COMPLAINT",
            "",
            "Subject:",
            subject,
            "",
            "Respected Sir/Madam,",
            "",
            "I am writing to report a cyber crime incident and request "
            "appropriate action regarding the matter described below.",
            "",
            "Incident Details:",
            "",
            f"Type of Incident: {incident_type}",
        ]

        if platform:
            lines.append(f"Platform: {platform}")

        if account_access:
            if str(account_access).lower() in {"no", "false", "unable", "locked out"}:
                lines.append("Current Account Status: Unable to access the account")
            else:
                lines.append(f"Current Account Status: {account_access}")

        if incident_date:
            lines.append(f"Date of Incident: {incident_date}")

        if payment_app:
            lines.append(f"Payment App: {payment_app}")

        if amount_lost:
            lines.append(f"Amount Involved: {amount_lost}")

        if transaction_date:
            lines.append(f"Transaction Date: {transaction_date}")

        if caller_identity:
            lines.append(f"Caller Claimed Identity: {caller_identity}")

        if caller_phone:
            lines.append(f"Caller Phone Number: {caller_phone}")

        lines.extend([
            "",
            "Incident Description:",
            "",
            description,
        ])

        # Add only facts explicitly provided by the user.
        if suspicious_activity:
            lines.extend([
                "",
                "Unauthorized / Suspicious Activity:",
                str(suspicious_activity),
            ])

        if otp_shared:
            lines.append(f"OTP Shared: {otp_shared}")

        if money_deducted:
            lines.append(f"Money Deducted: {money_deducted}")

        if money_transferred:
            lines.append(f"Money Transferred: {money_transferred}")

        if personal_information_shared:
            lines.append(
                f"Personal Information Shared: "
                f"{personal_information_shared}"
            )

        lines.extend([
            "",
            "Request:",
            "",
            "I request the concerned authorities to kindly register "
            "and investigate this complaint, identify the person(s) "
            "responsible for the unauthorized activity, and take "
            "appropriate action in accordance with applicable law.",
            "",
            "I am willing to provide any additional information, "
            "screenshots, emails, messages, transaction records, "
            "login alerts, or other evidence required for the "
            "investigation.",
            "",
            "Declaration:",
            "",
            "I confirm that the information provided in this complaint "
            "is true and correct to the best of my knowledge.",
            "",
            "Name: [Your Full Name]",
            "Contact Number: [Your Phone Number]",
            "Email Address: [Your Email Address]",
        ])

        if platform:
            lines.append(f"{platform} Username / Profile: [If applicable]")

        lines.extend([
            f"Date: {incident_date or '[Date of Incident]'}",
            "Place: [City, State]",
            "",
            "Disclaimer:",
            "",
            "This is an AI-generated draft intended for user review. "
            "It does not replace an official complaint form or legal "
            "documentation. Please verify all information before "
            "submitting it to any authority.",
        ])

        context.selected_document = "cyber_complaint"
        context.generated_document = "\n".join(lines)

        return context
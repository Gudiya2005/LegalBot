from app.agents.base_agent import BaseAgent


class ResponseFormatterAgent(BaseAgent):

    def __init__(self):
        super().__init__("Response Formatter")

    def execute(self, context):

        response = []

        # -----------------------------------------
        # Scam Checker
        # -----------------------------------------

        if getattr(context, "tool", "main") == "scam":

            # Gemini already creates the complete Scam Checker
            # response. Do not append generic emergency/evidence
            # sections because that creates duplicate information.
            context.final_response = (
                context.main_response.strip()
                if context.main_response
                else "Please describe the suspicious message, call, link, or situation you want me to check."
            )

            return context

        # -----------------------------------------
        # Complaint Draft Tool
        # -----------------------------------------

        if context.complaint_requested:

            if context.generated_document:

                context.final_response = (
                    "📄 Generated Complaint:\n\n"
                    + context.generated_document.strip()
                )

            else:

                context.final_response = (
                    context.main_response.strip()
                    if context.main_response
                    else "Please provide the missing information needed to prepare the complaint."
                )

            return context

        # -----------------------------------------
        # Emergency Help Tool
        # -----------------------------------------

        if context.emergency:

            if context.main_response:

                main_response = context.main_response.strip()

                # Remove empty numbered questions such as:
                # "1."
                # "2)"
                # "Question 1:"
                import re

                main_response = re.sub(
                    r"(?m)^\s*(?:\d+[\.\)]|Question\s+\d+\s*:?)\s*$",
                    "",
                    main_response
                )

                # Remove empty bullet points
                main_response = re.sub(
                    r"(?m)^\s*[-•]\s*$",
                    "",
                    main_response
                )

                # Clean excessive blank lines
                main_response = re.sub(
                    r"\n{3,}",
                    "\n\n",
                    main_response
                ).strip()

                response.append(main_response)

            # Do not append actions if Gemini has already
            # included an Immediate Actions section.
            main_lower = (
                context.main_response.lower()
                if context.main_response
                else ""
            )

            if (
                context.golden_hour_actions
                and "immediate actions" not in main_lower
            ):

                unique_actions = list(
                    dict.fromkeys(
                        context.golden_hour_actions
                    )
                )

                response.append(
                    "\n⚡ Immediate Actions:"
                )

                for action in unique_actions:
                    response.append(
                        f"• {action}"
                    )

            context.final_response = "\n".join(
                response
            ).strip()

            return context

        # -----------------------------------------
        # Evidence Guide Tool
        # -----------------------------------------

        if context.tool == "evidence":

            response = []

            if context.main_response:
                response.append(
                    context.main_response.strip()
                )

            # Do not append evidence if Gemini has already
            # provided an evidence section.
            main_lower = (
                context.main_response.lower()
                if context.main_response
                else ""
            )

            evidence_section_exists = any(
                phrase in main_lower
                for phrase in [
                    "evidence to preserve",
                    "preserve this evidence",
                    "evidence to collect",
                    "evidence to keep"
                ]
            )

            if (
                context.evidence_checklist
                and not evidence_section_exists
            ):

                response.append(
                    "\n📸 Evidence to Preserve:"
                )

                unique_evidence = list(
                    dict.fromkeys(
                        context.evidence_checklist
                    )
                )

                for item in unique_evidence:
                    response.append(
                        f"• {item}"
                    )

            context.final_response = "\n".join(
                response
            ).strip()

            return context

        # -----------------------------------------
        # Main Chat
        # -----------------------------------------
        #
        # Main Chat has two different response modes:
        #
        # 1. General cyber/legal question
        #    -> educational answer only
        #
        # 2. Actual cyber incident
        #    -> incident type + guidance + actions +
        #       evidence + necessary questions
        #
        # Specialized agents above are intentionally untouched.
        # -----------------------------------------

        if context.main_response:
            main_response = context.main_response.strip()

            # Remove empty numbered questions such as:
            # "3."
            # "3)"
            # "Question 3:"
            # while keeping all valid questions unchanged.
            import re

            main_response = re.sub(
                r"(?m)^\s*(?:\d+[\.\)]|Question\s+\d+\s*:?)\s*$",
                "",
                main_response
            )

            # Remove empty bullet points.
            main_response = re.sub(
                r"(?m)^\s*[-•]\s*$",
                "",
                main_response
            )

            # Remove excessive blank lines created by the cleanup.
            main_response = re.sub(
                r"\n{3,}",
                "\n\n",
                main_response
            ).strip()

            # Keep the existing behavior.
            if "Did you share" in main_response:
                main_response = main_response.split(
                    "Did you share"
                )[0].strip()

            response.append(main_response)

        main_lower = (
            context.main_response.lower()
            if context.main_response
            else ""
        )

        # -----------------------------------------
        # Determine whether this is a general query
        # -----------------------------------------

        is_general_query = getattr(
            context,
            "is_general_query",
            False
        )

        # -----------------------------------------
        # General Cyber / Legal Knowledge Question
        # -----------------------------------------
        #
        # Examples:
        # - What is phishing?
        # - What is hacking?
        # - What is the IT Act?
        # - What is digital arrest?
        #
        # Do NOT add incident-specific sections to
        # educational questions.
        # -----------------------------------------

        if is_general_query:

            # The answer from Gemini is the primary response.
            # Do not append:
            # - Incident Type
            # - Immediate Actions
            # - Evidence
            # - Incident questions
            #
            # This prevents a simple educational question
            # from looking like an active cybercrime case.

            context.final_response = "\n".join(
                response
            ).strip()

            return context

        # -----------------------------------------
        # Actual Cyber Incident
        # -----------------------------------------

        # -----------------------------------------
        # Incident Type
        # -----------------------------------------

        incident_type_value = (
            context.incident_type
            or context.intent
        )

        if incident_type_value:

            incident_type = (
                str(incident_type_value)
                .replace("_", " ")
                .strip()
            )

            already_present = (
                incident_type.lower()
                in main_lower
            )

            if not already_present:

                response.insert(
                    0,
                    f"🚨 Incident Type: {incident_type}"
                )

        # -----------------------------------------
        # Immediate Actions
        # -----------------------------------------

        # Gemini may already have provided these.
        # Only add the formatter's checklist if it has not.
        if (
            context.golden_hour_actions
            and "immediate actions" not in main_lower
        ):

            unique_actions = list(
                dict.fromkeys(
                    context.golden_hour_actions
                )
            )

            response.append(
                "\n⚡ Immediate Actions:"
            )

            for action in unique_actions:
                response.append(
                    f"• {action}"
                )

        # -----------------------------------------
        # Missing Information
        # -----------------------------------------

        # Only ask questions when Gemini/agents actually
        # identify missing information.
        #
        # Conversation history is handled upstream and
        # context.missing_information should represent
        # information still needed.
        #
        # Never append questions if Gemini already asked
        # a question in its response.

        if context.missing_information and "?" not in main_lower:

            question_map = {

                "platform":
                    "Which platform or account was affected?",

                "account_access":
                    "Can you still access your account?",

                "incident_date":
                    "When did you notice the incident?",

                "suspicious_activity":
                    "Have you noticed any unusual posts, messages, or changes to your profile?",

                "recovery_attempts":
                    "Have you tried recovering the account through the official recovery process?",

                "payment_app":
                    "Which payment app was involved?",

                "amount_lost":
                    "How much money was lost?",

                "transaction_date":
                    "When did the transaction happen?",

                "otp_shared":
                    "Did you share the OTP?",

                "money_deducted":
                    "Was any money deducted?",

                "caller_identity":
                    "What did the caller claim to be?",

                "caller_phone":
                    "Do you have the caller's phone number?",

                "money_transferred":
                    "Did you transfer any money?",

                "incident_description":
                    "Could you briefly describe what happened?"
            }

            questions = []

            for item in context.missing_information:

                question = question_map.get(
                    item,
                    item.replace("_", " ").capitalize() + "?"
                )

                if (
                    question not in questions
                    and question.lower() not in main_lower
                ):
                    questions.append(question)

            # Maximum of two follow-up questions.
            # The model should not turn every response into
            # a long questionnaire.
            if questions:

                response.append(
                    "\n❓ A little more information:"
                )

                for question in questions[:2]:

                    response.append(
                        f"• {question}"
                    )

        # -----------------------------------------
        # Evidence
        # -----------------------------------------

        evidence_section_exists = any(
            phrase in main_lower
            for phrase in [
                "evidence to preserve",
                "preserve this evidence",
                "evidence to collect",
                "evidence to keep"
            ]
        )

        if (
            context.evidence_checklist
            and not evidence_section_exists
        ):

            unique_evidence = list(
                dict.fromkeys(
                    context.evidence_checklist
                )
            )

            if unique_evidence:

                response.append(
                    "\n📸 Evidence to Preserve:"
                )

                for evidence in unique_evidence:

                    response.append(
                        f"• {evidence}"
                    )

        # -----------------------------------------
        # Knowledge
        # -----------------------------------------

        if context.retrieved_knowledge:

            response.append(
                "\n📚 Relevant Information:"
            )

            response.append(
                "Relevant information has been retrieved "
                "from the LegalBot Knowledge Base."
            )

        # -----------------------------------------
        # Generated Complaint
        # -----------------------------------------

        if context.generated_document:

            response.append(
                "\n📄 Generated Complaint:"
            )

            response.append(
                context.generated_document.strip()
            )

        # -----------------------------------------
        # Final response
        # -----------------------------------------

        context.final_response = "\n".join(
            response
        ).strip()

        return context
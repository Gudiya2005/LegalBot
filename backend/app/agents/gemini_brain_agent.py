from app.agents.base_agent import BaseAgent
from app.services.cyber_brain_service import ask_cyber_brain


class GeminiBrainAgent(BaseAgent):

    def __init__(self):
        super().__init__("Gemini Cyber Brain")

    def execute(self, context):

        result = ask_cyber_brain(
            message=context.message,
            history=context.chat_history,
            knowledge=context.retrieved_knowledge,
            tool=context.tool
        )

        # -----------------------------------------
        # Language
        # -----------------------------------------

        context.language = result.get(
            "language",
            context.language or "en"
        )

        # -----------------------------------------
        # Cyber classification
        # -----------------------------------------

        context.is_cyber_related = result.get(
            "is_cyber_related",
            context.is_cyber_related
        )

        context.is_new_incident = result.get(
            "is_new_incident",
            context.is_new_incident
        )

        context.is_general_query = result.get(
            "is_general_query",
            context.is_general_query
        )

        context.emergency = result.get(
            "is_emergency",
            context.emergency
        )

        # -----------------------------------------
        # Incident type
        # -----------------------------------------

        incident_type = result.get(
            "incident_type"
        )

        if incident_type:
            context.incident_type = incident_type
            context.intent = incident_type

        elif not context.incident_type:
            context.incident_type = "Cyber Crime"
            context.intent = "Cyber Crime"

        # -----------------------------------------
        # Collected information
        # -----------------------------------------

        extracted = result.get(
            "collected_information",
            {}
        )

        if isinstance(extracted, dict):
            context.collected_information.update(
                extracted
            )

        # -----------------------------------------
        # Missing information
        # -----------------------------------------

        missing = result.get(
            "missing_information"
        )

        if isinstance(missing, list):
            context.missing_information = missing

        context.information_complete = (
            len(context.missing_information) == 0
        )

        # -----------------------------------------
        # Immediate actions
        # -----------------------------------------

        actions = result.get(
            "immediate_actions"
        )

        if isinstance(actions, list):
            context.golden_hour_actions = actions

        # -----------------------------------------
        # Evidence
        # -----------------------------------------

        evidence = result.get(
            "evidence"
        )

        if isinstance(evidence, list):
            context.evidence_checklist = evidence

        # -----------------------------------------
        # Complaint
        # -----------------------------------------

        # Once requested, don't accidentally reset it
        # during a follow-up message.

        if result.get("complaint_requested") is True:
            context.complaint_requested = True

        if result.get("complaint_ready") is True:
            context.complaint_ready = True

        # -----------------------------------------
        # Gemini response
        # -----------------------------------------

        response = result.get(
            "response"
        )

        if response:
            context.main_response = response

        return context
from pathlib import Path

from app.agents.base_agent import BaseAgent


class DocumentGeneratorAgent(BaseAgent):

    def __init__(self):
        super().__init__("Document Generator")

    def execute(self, context):

        if not context.response_plan.get(
            "generate_document"
        ):
            return context


        if not context.information_complete:

            context.generated_document = ""

            return context


        # -----------------------------------------
        # Default document
        # -----------------------------------------

        if not context.selected_document:

            context.selected_document = (
                "cyber_complaint"
            )


        template_path = (
            Path(__file__).parent.parent
            / "templates"
            / f"{context.selected_document}.txt"
        )


        # -----------------------------------------
        # Fallback
        # -----------------------------------------

        if (
            not template_path.exists()
            or template_path.stat().st_size == 0
        ):

            template_path = (
                Path(__file__).parent.parent
                / "templates"
                / "cyber_complaint.txt"
            )


        if (
            not template_path.exists()
            or template_path.stat().st_size == 0
        ):

            context.generated_document = (
                "No document template is currently available."
            )

            return context


        template = template_path.read_text(
            encoding="utf-8"
        )


        # -----------------------------------------
        # Build incident details
        # -----------------------------------------

        information = (
            context.collected_information
        )


        incident_details = []


        if information.get("platform"):

            incident_details.append(
                f"Social media platform: "
                f"{information['platform']}"
            )


        if information.get("account_access"):

            access = information[
                "account_access"
            ]

            if str(access).lower() in [
                "no",
                "false",
                "cannot access",
                "unable to access"
            ]:

                access_text = (
                    "No, the user cannot access "
                    "the account."
                )

            else:

                access_text = (
                    f"The user can access "
                    f"the account: {access}"
                )

            incident_details.append(
                f"Account access: {access_text}"
            )


        if information.get("incident_date"):

            incident_details.append(
                f"Incident date: "
                f"{information['incident_date']}"
            )


        if information.get("payment_app"):

            incident_details.append(
                f"Payment app: "
                f"{information['payment_app']}"
            )


        if information.get("amount_lost"):

            incident_details.append(
                f"Amount lost: "
                f"{information['amount_lost']}"
            )


        if information.get("transaction_date"):

            incident_details.append(
                f"Transaction date: "
                f"{information['transaction_date']}"
            )


        if information.get("otp_shared"):

            incident_details.append(
                f"OTP shared: "
                f"{information['otp_shared']}"
            )


        if information.get("money_deducted"):

            incident_details.append(
                f"Money deducted: "
                f"{information['money_deducted']}"
            )


        incident_details_text = "\n".join(
            incident_details
        )


        # -----------------------------------------
        # Generate document
        # -----------------------------------------

        context.generated_document = template.format(

            intent=context.intent.replace(
                "_",
                " "
            ).title(),

            message=incident_details_text,

            evidence=(
                "\n- "
                + "\n- ".join(
                    context.evidence_checklist
                )
            ),

            knowledge=context.retrieved_knowledge
        )


        return context
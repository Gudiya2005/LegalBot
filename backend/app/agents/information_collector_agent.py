from app.agents.base_agent import BaseAgent
from app.services.information_extractor import extract_information


class InformationCollectorAgent(BaseAgent):

    def __init__(self):
        super().__init__("Information Collector")

    def execute(self, context):

        questions = {

            "social_media_hacking": {
                "platform":
                    "Which social media platform was hacked?",

                "account_access":
                    "Can you still access your account?",

                "incident_date":
                    "When did the incident happen?"
            },

            "upi_fraud": {
                "payment_app":
                    "Which payment app was used?",

                "amount_lost":
                    "How much money was lost?",

                "transaction_date":
                    "When did the transaction happen?"
            },

            "otp_fraud": {
                "otp_shared":
                    "Did you share the OTP?",

                "money_deducted":
                    "Was any money deducted?"
            }
        }


        # Emergency incidents don't require
        # normal information collection.
        if context.emergency:
            return context


        required_fields = questions.get(
            context.intent,
            {}
        )


        # Unknown/general incident
        if not required_fields:

            context.missing_information = []
            context.information_complete = True

            return context


        # -----------------------------------------
        # Build previous user conversation
        # -----------------------------------------

        previous_user_messages = []

        for chat in context.chat_history:

            if chat["role"] == "user":

                previous_user_messages.append(
                    chat["message"]
                )


        # -----------------------------------------
        # Extract previous information
        # -----------------------------------------

        if previous_user_messages:

            previous_conversation = "\n".join(
                previous_user_messages
            )

            previous_extracted = extract_information(
                message=previous_conversation,
                intent=context.intent,
                missing_information=list(
                    required_fields.values()
                ),
                previous_information={},
                chat_history=context.chat_history
            )

            context.collected_information.update(
                previous_extracted
            )


        # -----------------------------------------
        # Extract current message
        # -----------------------------------------

        extracted = extract_information(
            message=context.message,
            intent=context.intent,
            missing_information=list(
                required_fields.values()
            ),
            previous_information=
                context.collected_information,

            chat_history=context.chat_history
        )


        # -----------------------------------------
        # Merge information
        # -----------------------------------------

        context.collected_information.update(
            extracted
        )


        # -----------------------------------------
        # Determine missing information
        # -----------------------------------------

        context.missing_information = [

            question

            for field, question
            in required_fields.items()

            if not context.collected_information.get(field)
        ]


        context.information_complete = (
            len(context.missing_information) == 0
        )


        return context
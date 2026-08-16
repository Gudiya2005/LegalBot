from app.agents.base_agent import BaseAgent
from app.agents.intent_classifier import classify_intent


class IntentAgent(BaseAgent):

    def __init__(self):
        super().__init__("Intent Classification Agent")

    def execute(self, context):

        # -------------------------------------------------
        # 1. Classify the CURRENT message
        # -------------------------------------------------

        current_intent = classify_intent(
            context.message
        )

        # -------------------------------------------------
        # 2. If current message clearly identifies an
        #    incident, use that intent.
        # -------------------------------------------------

        if current_intent != "general":

            context.intent = current_intent

            return context

        # -------------------------------------------------
        # 3. Current message is vague/general.
        #    Look at previous USER messages.
        # -------------------------------------------------

        previous_user_messages = []

        for chat in context.chat_history:

            if chat["role"] == "user":

                previous_user_messages.append(
                    chat["message"]
                )

        # -------------------------------------------------
        # 4. Find the most recent known incident intent.
        # -------------------------------------------------

        previous_intent = "general"

        for message in reversed(
            previous_user_messages
        ):

            detected_intent = classify_intent(
                message
            )

            if detected_intent != "general":

                previous_intent = detected_intent

                break

        # -------------------------------------------------
        # 5. If current message is vague and there is a
        #    previous incident, treat it as a continuation.
        # -------------------------------------------------

        if previous_intent != "general":

            context.intent = previous_intent

        else:

            context.intent = current_intent

        return context
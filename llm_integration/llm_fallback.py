"""
LLM Fallback Action for handling unknown intents
"""
import logging
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted

from .llm_client import get_llm_client
from .context_manager import get_context_manager
from .config import get_llm_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ActionLLMFallback(Action):
    """
    Fallback action that uses an LLM to handle unknown intents
    """

    def name(self) -> Text:
        return "action_llm_fallback"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        """
        Execute the fallback action using LLM

        Args:
            dispatcher: Dispatcher to send messages back to user
            tracker: Current conversation tracker
            domain: Domain definition

        Returns:
            List of events
        """
        config = get_llm_config()

        # Get the user message
        user_message = tracker.latest_message.get("text", "")

        # Get or create a session ID
        session_id = tracker.sender_id

        # Get the conversation context
        context_manager = get_context_manager()

        # Get business type from context or tracker slots
        business_type = context_manager.get_business_type(session_id)
        if not business_type and tracker.get_slot("business_type"):
            business_type = tracker.get_slot("business_type")
            context_manager.set_business_type(session_id, business_type)

        # Add system prompt with business context
        system_prompt = self._build_system_prompt(business_type)
        context = context_manager.get_context_for_llm(session_id)

        if system_prompt:
            # Insert system prompt at the beginning if context isn't empty
            context.insert(0, {"role": "system", "content": system_prompt})

        # Add the current user message to the context
        context_manager.add_user_message(session_id, user_message)

        # Get an LLM client
        llm_client = get_llm_client()

        # Generate a response using the LLM
        try:
            llm_response = llm_client.generate_response(user_message, context)

            # Send the response to the user
            dispatcher.utter_message(text=llm_response)

            # Add the assistant's response to the context
            context_manager.add_assistant_message(session_id, llm_response)

            # Log the interaction
            logger.info(f"LLM Fallback: User message: '{user_message}', Response: '{llm_response}'")

        except Exception as e:
            logger.error(f"Error using LLM fallback: {e}")
            dispatcher.utter_message(text="I'm having trouble understanding. Could you rephrase your question?")

        # Return UserUtteranceReverted() to not influence further conversation
        return [UserUtteranceReverted()]

    def _build_system_prompt(self, business_type: str = None) -> str:
        """
        Build a system prompt based on the business type

        Args:
            business_type (str, optional): The business type

        Returns:
            str: The system prompt
        """
        base_prompt = (
            "You are a helpful assistant for a business. "
            "Your answers should be concise, helpful, and professional. "
        )

        if business_type == "healthcare":
            return base_prompt + (
                "This is a healthcare business. Remember to be empathetic and remind users "
                "that you cannot provide medical advice, diagnosis, or treatment recommendations. "
                "For specific medical concerns, always suggest consulting with a healthcare professional."
            )
        elif business_type == "retail":
            return base_prompt + (
                "This is a retail business. Focus on helping customers with product information, "
                "order tracking, returns, and general shopping assistance. Be friendly and solution-oriented."
            )
        elif business_type == "finance":
            return base_prompt + (
                "This is a financial services business. Be precise and clear in your responses. "
                "Remember to note that you cannot provide specific financial advice or investment recommendations. "
                "For personalized financial guidance, suggest consulting with a financial advisor."
            )
        else:
            return base_prompt + (
                "Provide helpful, accurate information. If you don't know the answer to a question, "
                "acknowledge this and suggest how the user might find the information they're looking for."
            )
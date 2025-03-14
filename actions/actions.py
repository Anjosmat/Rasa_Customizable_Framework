import logging
from typing import Any, Text, Dict, List
from datetime import datetime

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from database.db_config import SessionLocal, BusinessIntent, BotConfig, Business
from admin.models import ChatbotLog

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ActionRespondFromDB(Action):
    """
    Action to fetch and respond with the appropriate response text from the database
    based on the detected intent and business type.
    """

    def name(self) -> Text:
        return "action_respond_from_db"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        session = SessionLocal()

        # Get the intent from the latest message
        user_intent = tracker.latest_message.get("intent", {}).get("name")
        user_message = tracker.latest_message.get("text")

        # Get business type from slot (defaulting to 'general' if not set)
        business_type = tracker.get_slot("business_type") or "general"

        logger.info(f"Received intent: {user_intent} for business type: {business_type}")

        try:
            # Try to find the exact business type and intent match
            intent_data = session.query(BusinessIntent).filter_by(
                business_type=business_type, intent_name=user_intent
            ).first()

            # If not found, try to find a general response for the intent
            if not intent_data and business_type != "general":
                intent_data = session.query(BusinessIntent).filter_by(
                    business_type="general", intent_name=user_intent
                ).first()

            # Get business for logging
            business = session.query(Business).filter_by(business_type=business_type).first()
            business_id = business.id if business else None

            # If we found a response, use it
            if intent_data:
                response = intent_data.response_text
                dispatcher.utter_message(text=response)
                logger.info(f"Responding with: {response}")

                # Log this interaction
                self._log_interaction(session, business_id, user_message, response, user_intent)
            else:
                # Use fallback response from config or default
                config = session.query(BotConfig).filter_by(business_type=business_type).first()

                if config:
                    fallback = config.default_fallback
                else:
                    fallback = "I'm not sure how to respond to that."

                dispatcher.utter_message(text=fallback)
                logger.warning(f"No response found for intent: {user_intent}")

                # Log this interaction
                self._log_interaction(session, business_id, user_message, fallback, user_intent)

        except Exception as e:
            logger.error(f"Error retrieving intent response: {e}")
            dispatcher.utter_message(text="An error occurred while processing your request.")
        finally:
            session.close()

        return []

    def _log_interaction(self, session, business_id, user_message, bot_response, intent_detected):
        """Helper method to log the interaction"""
        try:
            log = ChatbotLog(
                business_id=business_id,
                user_message=user_message,
                bot_response=bot_response,
                intent_detected=intent_detected,
                timestamp=datetime.now().isoformat()
            )
            session.add(log)
            session.commit()
        except Exception as e:
            logger.error(f"Error logging interaction: {e}")
            session.rollback()


class ActionSetBusinessType(Action):
    """
    Action to set the business type based on user input
    """

    def name(self) -> Text:
        return "action_set_business_type"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract business type from entities
        business_type = next(tracker.get_latest_entity_values("business_type"), None)

        if business_type:
            # Check if this business type exists in the database
            session = SessionLocal()
            db_business = session.query(Business).filter_by(business_type=business_type).first()

            if db_business:
                dispatcher.utter_message(text=f"I've set your business type to {business_type}.")
                session.close()
                return [SlotSet("business_type", business_type)]

            session.close()
            dispatcher.utter_message(text=f"I don't recognize {business_type} as a valid business type.")
        else:
            dispatcher.utter_message(text="I couldn't detect a business type from your message.")

        return []


class ActionListIntents(Action):
    """
    Action to list available intents for the current business type
    """

    def name(self) -> Text:
        return "action_list_intents"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get business type from slot
        business_type = tracker.get_slot("business_type") or "general"

        session = SessionLocal()
        try:
            # Get intents for this business type
            intents = session.query(BusinessIntent).filter_by(business_type=business_type).all()

            if intents:
                intent_list = "\n".join([f"- {intent.intent_name}" for intent in intents])
                dispatcher.utter_message(text=f"Here are the available intents for {business_type}:\n{intent_list}")
            else:
                dispatcher.utter_message(text=f"No specific intents found for {business_type}.")
        except Exception as e:
            logger.error(f"Error retrieving intents: {e}")
            dispatcher.utter_message(text="An error occurred while retrieving intents.")
        finally:
            session.close()

        return []
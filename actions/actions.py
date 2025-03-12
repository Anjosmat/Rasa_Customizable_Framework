import logging
from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from database.models import DBIntent, DBResponse
from database.db_config import SessionLocal

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ActionRespondFromDB(Action):
    """Action to fetch and deliver responses from the database based on detected intent."""

    def name(self) -> Text:
        """Return the name of the action."""
        return "action_respond_from_db"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        """
        Execute the action to respond from database.

        Args:
            dispatcher: Used to send messages back to the user
            tracker: Current conversation state
            domain: Bot's domain configuration

        Returns:
            Empty list of events
        """
        session = SessionLocal()
        user_intent = tracker.latest_message["intent"].get("name")

        logger.info(f"Received intent: {user_intent}")

        try:
            intent_data = session.query(DBIntent).filter_by(name=user_intent).first()
            if intent_data:
                response_data = session.query(DBResponse).filter_by(intent_id=intent_data.id).first()
                if response_data:
                    response = response_data.content
                    dispatcher.utter_message(text=response)
                    logger.info(f"Responding with: {response}")
                else:
                    dispatcher.utter_message(text="I'm not sure how to respond to that.")
                    logger.warning(f"No response found in DBResponse for intent: {user_intent}")
            else:
                dispatcher.utter_message(text="I'm not sure how to respond to that.")
                logger.warning(f"No intent found in DBIntent named: {user_intent}")
        except Exception as e:
            logger.error(f"Error retrieving intent response: {e}")
            dispatcher.utter_message(text="An error occurred while processing your request.")
        finally:
            session.close()

        return []

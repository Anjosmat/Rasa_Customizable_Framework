import logging
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from sqlalchemy.orm import sessionmaker
from database.db_config import SessionLocal, BusinessIntent

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ActionRespondFromDB(Action):
    def name(self):
        return "action_respond_from_db"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        session = SessionLocal()
        user_intent = tracker.latest_message["intent"].get("name")

        logger.info(f"Received intent: {user_intent}")

        try:
            intent_data = session.query(BusinessIntent).filter_by(intent_name=user_intent).first()
            if intent_data:
                response = intent_data.response_text
                dispatcher.utter_message(text=response)
                logger.info(f"Responding with: {response}")
            else:
                dispatcher.utter_message(text="I'm not sure how to respond to that.")
                logger.warning(f"No response found for intent: {user_intent}")
        except Exception as e:
            logger.error(f"Error retrieving intent response: {e}")
            dispatcher.utter_message(text="An error occurred while processing your request.")
        finally:
            session.close()

        return []

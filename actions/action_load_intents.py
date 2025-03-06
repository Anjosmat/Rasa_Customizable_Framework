from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from database.db_config import SessionLocal, BusinessIntent


class ActionLoadBusinessIntents(Action):
    def name(self) -> Text:
        return "action_load_business_intents"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Retrieve the business type from a slot
        business_type = tracker.get_slot("business_type")
        if not business_type:
            dispatcher.utter_message(text="I couldn't determine your business type.")
            return []

        # Connect to the database and fetch intents
        db = SessionLocal()
        intents = db.query(BusinessIntent).filter(BusinessIntent.business_type == business_type).all()
        db.close()

        if not intents:
            dispatcher.utter_message(text=f"No predefined responses found for business type: {business_type}.")
            return []

        # For each intent found, send a message (this is just an example)
        for intent in intents:
            dispatcher.utter_message(
                text=f"Intent: {intent.intent_name} → Response: {intent.response_text}"
            )

        return []

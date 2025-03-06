import sqlite3
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionRespondFromDatabase(Action):
    def name(self) -> Text:
        return "action_respond_from_db"

    def fetch_response_from_db(self, intent_name: Text) -> Text:
        """Fetches response from SQLite database based on intent"""
        conn = sqlite3.connect("chatbot.db")
        cursor = conn.cursor()

        cursor.execute("SELECT response FROM intents WHERE intent_name=?", (intent_name,))
        result = cursor.fetchone()

        conn.close()
        return result[0] if result else "Sorry, I don't understand that."

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        """Handles user intent dynamically from the database"""
        intent = tracker.latest_message["intent"]["name"]
        response = self.fetch_response_from_db(intent)

        dispatcher.utter_message(text=response)
        return []

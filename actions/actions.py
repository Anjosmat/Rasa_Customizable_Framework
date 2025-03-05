import json
import os
from rasa_sdk import Action
from rasa_sdk.events import SlotSet


# Load intents dynamically
class ActionLoadBusinessIntents(Action):{
    "intents": [
        {
            "name": "schedule_appointment",
            "examples": [{
    "intents": [
        {
            "name": "open_bank_account",
            "examples": [
                "I want to open a bank account",
                "How can I create a new account?",
                "What are the requirements for a new account?"
            ]
        },
        {
            "name": "loan_application",
            "examples": [
                "How do I apply for a loan?",
                "Can I get a personal loan?",
                "Tell me about home loan options."
            ]
        }
    ]
}

                "I want to schedule an appointment",
                "Book a doctor visit",
                "Can I see a doctor on Monday?"
            ]
        },
        {
            "name": "symptom_checker",
            "examples": [
                "I have a headache and fever",
                "My throat hurts, what should I do?",
                "What are the symptoms of flu?"
            ]
        }
    ]
}

    def name(self):
        return "action_load_business_intents"

    def run(self, dispatcher, tracker, domain):
        user_id = tracker.get_slot("user_id")
        business_type = tracker.get_slot("business_type")

        # Load intents from JSON file
        intents_path = f"data/intents/{business_type}.json"

        if os.path.exists(intents_path):
            with open(intents_path, "r") as file:
                intents_data = json.load(file)
                dispatcher.utter_message(text="Business intents loaded successfully.")
                return [SlotSet("business_intents", intents_data)]
        else:
            dispatcher.utter_message(text="No intents found for this business type.")
            return []

from sqlalchemy.orm import Session
from database.db_config import SessionLocal, BusinessIntent

def load_sample_data():
    session: Session = SessionLocal()

    # Clear existing data
    session.query(BusinessIntent).delete()

    sample_intents = [
        {"business_type": "healthcare", "intent_name": "schedule_appointment", "response_text": "Sure! What day and time works for you?"},
        {"business_type": "retail", "intent_name": "track_order", "response_text": "Please provide your order number, and I will check it for you."},
        {"business_type": "finance", "intent_name": "open_bank_account", "response_text": "I can help with that. Do you prefer a savings or checking account?"}
    ]

    for intent in sample_intents:
        new_intent = BusinessIntent(**intent)
        session.add(new_intent)

    session.commit()
    session.close()
    print("Sample data inserted successfully!")

if __name__ == "__main__":
    load_sample_data()

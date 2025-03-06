from database.db_config import SessionLocal, BusinessIntent


def check_database():
    db = SessionLocal()
    intents = db.query(BusinessIntent).all()

    if not intents:
        print("No data found in the database.")
    else:
        print("Database contents:")
        for intent in intents:
            print(
                f"Business Type: {intent.business_type}, Intent: {intent.intent_name}, Response: {intent.response_text}")

    db.close()


if __name__ == "__main__":
    check_database()

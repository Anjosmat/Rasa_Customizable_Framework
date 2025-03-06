import yaml
from database.db_config import SessionLocal
from database.models import BusinessIntent

def generate_nlu_file():
    session = SessionLocal()
    try:
        intents = session.query(BusinessIntent).all()
        nlu_data = {"version": "3.1", "nlu": []}

        for intent in intents:
            nlu_data["nlu"].append({
                "intent": intent.intent_name,
                "examples": "- " + "\n- ".join(intent.training_examples.split(";"))
            })

        with open("data/nlu.yml", "w", encoding="utf-8") as file:
            yaml.dump(nlu_data, file, allow_unicode=True, default_flow_style=False)

        print("✅ nlu.yml generated successfully!")

    finally:
        session.close()

if __name__ == "__main__":
    generate_nlu_file()

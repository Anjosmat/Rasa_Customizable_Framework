from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.models import Intent
from app.schemas.intent import IntentCreate, IntentUpdate


def create_intent(db: Session, intent: IntentCreate) -> Intent:
    db_intent = Intent(**intent.dict())
    db.add(db_intent)
    db.commit()
    db.refresh(db_intent)
    return db_intent


def get_intent(db: Session, intent_id: int) -> Optional[Intent]:
    return db.query(Intent).filter(Intent.id == intent_id).first()


def get_intents(db: Session, skip: int = 0, limit: int = 100) -> List[Intent]:
    return db.query(Intent).offset(skip).limit(limit).all()


def update_intent(db: Session, intent_id: int, intent: IntentUpdate) -> Optional[Intent]:
    db_intent = db.query(Intent).filter(Intent.id == intent_id).first()
    if db_intent:
        for key, value in intent.dict(exclude_unset=True).items():
            setattr(db_intent, key, value)
        db.commit()
        db.refresh(db_intent)
    return db_intent


def delete_intent(db: Session, intent_id: int) -> bool:
    intent = db.query(Intent).filter(Intent.id == intent_id).first()
    if intent:
        db.delete(intent)
        db.commit()
        return True
    return False

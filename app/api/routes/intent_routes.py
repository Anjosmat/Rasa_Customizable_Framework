from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.db_config import get_db
from app.schemas.intent import IntentCreate, IntentResponse, IntentUpdate
from app.crud import intent as intent_crud

router = APIRouter()


@router.post("/intents/", response_model=IntentResponse)
def create_intent(intent: IntentCreate, db: Session = Depends(get_db)):
    return intent_crud.create_intent(db=db, intent=intent)


@router.get("/intents/", response_model=List[IntentResponse])
def read_intents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    intents = intent_crud.get_intents(db, skip=skip, limit=limit)
    return intents


@router.get("/intents/{intent_id}", response_model=IntentResponse)
def read_intent(intent_id: int, db: Session = Depends(get_db)):
    intent = intent_crud.get_intent(db, intent_id=intent_id)
    if intent is None:
        raise HTTPException(status_code=404, detail="Intent not found")
    return intent


@router.put("/intents/{intent_id}", response_model=IntentResponse)
def update_intent(intent_id: int, intent: IntentUpdate, db: Session = Depends(get_db)):
    updated_intent = intent_crud.update_intent(db, intent_id=intent_id, intent=intent)
    if updated_intent is None:
        raise HTTPException(status_code=404, detail="Intent not found")
    return updated_intent


@router.delete("/intents/{intent_id}")
def delete_intent(intent_id: int, db: Session = Depends(get_db)):
    success = intent_crud.delete_intent(db, intent_id=intent_id)
    if not success:
        raise HTTPException(status_code=404, detail="Intent not found")
    return {"message": "Intent deleted successfully"}

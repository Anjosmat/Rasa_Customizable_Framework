from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .response import ResponseResponse


class IntentBase(BaseModel):
    name: str
    description: Optional[str] = None
    pattern: str
    is_active: bool = True


class IntentCreate(IntentBase):
    pass


class IntentUpdate(IntentBase):
    pass


class IntentResponse(IntentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    responses: List[ResponseResponse] = []

    class Config:
        orm_mode = True

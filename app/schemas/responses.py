from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ResponseBase(BaseModel):
    content: str
    response_type: str = "text"
    metadata: Optional[str] = None
    is_active: bool = True


class ResponseCreate(ResponseBase):
    intent_id: int


class ResponseUpdate(ResponseBase):
    pass


class ResponseResponse(ResponseBase):
    id: int
    intent_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

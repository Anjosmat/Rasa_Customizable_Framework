from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database.db_config import Base


class AdminIntent(Base):
    __tablename__ = 'admin_intents'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    pattern = Column(Text, nullable=False)  # Training phrases or regex pattern
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Relationship with responses
    responses = relationship('AdminResponse', back_populates='intent')


class AdminResponse(Base):
    __tablename__ = 'admin_responses'

    id = Column(Integer, primary_key=True)
    intent_id = Column(Integer, ForeignKey('admin_intents.id'), nullable=False)
    content = Column(Text, nullable=False)
    response_type = Column(String(50), default='text')  # text, button, card, etc.
    metadata = Column(Text)  # JSON field for additional data
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Relationship with intent
    intent = relationship('AdminIntent', back_populates='responses')

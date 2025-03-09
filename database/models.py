from sqlalchemy import Column, String, Integer, Boolean, create_engine, ForeignKey, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
import json

Base = declarative_base()


# Plugin System
@dataclass
class IntentPlugin:
    name: str
    handlers: List[callable] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def register_handler(self, handler: callable) -> None:
        self.handlers.append(handler)


# Event Handler
@dataclass
class DatabaseEventHandler:
    def on_intent_created(self, intent_id: int) -> None:
        pass

    def on_response_added(self, response_id: int) -> None:
        pass

    def on_config_updated(self, config_id: int) -> None:
        pass


# Existing Models with Enhancements
class BusinessIntent(Base):
    __tablename__ = "business_intents"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    business_type = Column(String, index=True)
    intent_name = Column(String, index=True)
    response_text = Column(String)

    # New fields for extensibility
    metadata = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    priority = Column(Integer, default=0)

    # Relationships
    custom_responses = relationship("CustomResponse", back_populates="intent")

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'business_type': self.business_type,
            'intent_name': self.intent_name,
            'response_text': self.response_text,
            'metadata': self.metadata,
            'priority': self.priority
        }


class BotConfig(Base):
    __tablename__ = "bot_config"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    business_type = Column(String, index=True)
    default_greeting = Column(String, default="Hello! Welcome!")
    default_fallback = Column(String, default="I'm not sure I understand.")
    enable_voice_support = Column(Boolean, default=True)
    enable_multilingual = Column(Boolean, default=True)

    # New fields for extensibility
    custom_settings = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    version = Column(String, default="1.0.0")

    def update_settings(self, settings: dict) -> None:
        self.custom_settings.update(settings)

    def get_setting(self, key: str, default: Any = None) -> Any:
        return self.custom_settings.get(key, default)


# New Models for Extensibility
class CustomResponse(Base):
    __tablename__ = "custom_responses"

    id = Column(Integer, primary_key=True, index=True)
    intent_id = Column(Integer, ForeignKey('business_intents.id'))
    response_type = Column(String, default="text")  # text, button, card, etc.
    response_content = Column(JSON)
    conditions = Column(JSON, default={})  # Conditions for when to use this response
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    intent = relationship("BusinessIntent", back_populates="custom_responses")


class IntentMetadata(Base):
    __tablename__ = "intent_metadata"

    id = Column(Integer, primary_key=True, index=True)
    intent_id = Column(Integer, ForeignKey('business_intents.id'))
    key = Column(String, index=True)
    value = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# Helper function for database initialization
def init_models(engine):
    Base.metadata.create_all(bind=engine)
    return SessionLocal()


# Create database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

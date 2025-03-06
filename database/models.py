from sqlalchemy import Column, String, Integer, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Define BusinessIntent model
class BusinessIntent(Base):
    __tablename__ = "business_intents"
    __table_args__ = {'extend_existing': True}  # Fix for redefinition issue

    id = Column(Integer, primary_key=True, index=True)
    business_type = Column(String, index=True)
    intent_name = Column(String, index=True)
    response_text = Column(String)

# Define BotConfig model
class BotConfig(Base):
    __tablename__ = "bot_config"
    __table_args__ = {'extend_existing': True}  # Fix for redefinition issue

    id = Column(Integer, primary_key=True, index=True)
    business_type = Column(String, index=True)
    default_greeting = Column(String, default="Hello! Welcome!")
    default_fallback = Column(String, default="I'm not sure I understand.")
    enable_voice_support = Column(Boolean, default=True)
    enable_multilingual = Column(Boolean, default=True)

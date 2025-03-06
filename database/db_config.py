from sqlalchemy import create_engine, Column, String, Integer, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

# Define the database file
DATABASE_URL = "sqlite:///database/business_data.db"

# Create engine and session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define BusinessIntent table
class BusinessIntent(Base):
    __tablename__ = "business_intents"
    id = Column(Integer, primary_key=True, index=True)
    business_type = Column(String, index=True)
    intent_name = Column(String, index=True)
    response_text = Column(String)

# Define BotConfig table
class BotConfig(Base):
    __tablename__ = "bot_config"
    id = Column(Integer, primary_key=True, index=True)
    business_type = Column(String, unique=True, index=True)
    default_greeting = Column(String)
    default_fallback = Column(String)
    enable_voice_support = Column(Boolean, default=True)
    enable_multilingual = Column(Boolean, default=True)

# Create tables in the database
Base.metadata.create_all(bind=engine)

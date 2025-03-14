from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

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
    training_examples = Column(String, default="")  # Examples separated by semicolons


# Define BotConfig table
class BotConfig(Base):
    __tablename__ = "bot_config"
    id = Column(Integer, primary_key=True, index=True)
    business_type = Column(String, unique=True, index=True)
    default_greeting = Column(String, default="Hello! Welcome!")
    default_fallback = Column(String, default="I'm not sure I understand.")
    enable_voice_support = Column(Boolean, default=True)
    enable_multilingual = Column(Boolean, default=True)


# Define Business table
class Business(Base):
    __tablename__ = "businesses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    business_type = Column(String, index=True)
    contact_email = Column(String)
    is_active = Column(Boolean, default=True)

    # Relationships
    intents = relationship("BusinessIntent",
                           primaryjoin="Business.business_type==BusinessIntent.business_type",
                           foreign_keys=[BusinessIntent.business_type],
                           viewonly=True)

    config = relationship("BotConfig",
                          primaryjoin="Business.business_type==BotConfig.business_type",
                          foreign_keys=[BotConfig.business_type],
                          viewonly=True)


# Create all tables in the database
def create_tables():
    Base.metadata.create_all(bind=engine)


# Get a new database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
DATABASE_URL = "sqlite:///./business_intents.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Define BusinessIntent model
class BusinessIntent(Base):
    __tablename__ = "business_intents"

    id = Column(Integer, primary_key=True, index=True)
    business_type = Column(String, index=True)
    intent_name = Column(String, index=True)
    response_text = Column(String)

# Create database tables
Base.metadata.create_all(bind=engine)

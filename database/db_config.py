from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create the SQLAlchemy engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./rasa_framework.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = SessionLocal

# Create declarative base
Base = declarative_base()


def init_db():
    """Initialize the database, creating all tables."""
    # Import all models here that need to be created
    from admin.models import AdminUser  # This ensures the model is registered
    from models import Intent, Response  # Import the new models

    Base.metadata.create_all(bind=engine)


def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

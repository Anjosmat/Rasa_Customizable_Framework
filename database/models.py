from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, JSON
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


class Business(Base):
    __tablename__ = 'businesses'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    api_key = Column(String, unique=True)
    config = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    intents = Column(JSON)
    bot_config = Column(JSON)


class DBIntent(Base):
    __tablename__ = 'db_intents'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    business_id = Column(Integer, ForeignKey('businesses.id'))
    name = Column(String)
    language = Column(String)
    category = Column(String)
    intent_metadata = Column(JSON)
    description = Column(String)
    priority = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)


class DBResponse(Base):
    __tablename__ = 'db_responses'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    intent_id = Column(Integer, ForeignKey('db_intents.id'))
    content = Column(String)
    response_type = Column(String)
    response_metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)


class CustomResponse(Base):
    __tablename__ = 'custom_responses'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    intent_id = Column(Integer, ForeignKey('db_intents.id'))
    response_type = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class BotConfig(Base):
    __tablename__ = 'bot_configs'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    business_id = Column(Integer, ForeignKey('businesses.id'))
    enable_voice_support = Column(Boolean)
    enable_multilingual = Column(Boolean)
    custom_settings = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    def update_settings(self, settings_dict):
        self.custom_settings.update(settings_dict)

    def get_setting(self, key, default=None):
        return self.custom_settings.get(key, default)


class IntentMetadata(Base):
    __tablename__ = 'intent_metadata'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    intent_id = Column(Integer, ForeignKey('db_intents.id'))
    key = Column(String)
    value = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


# Initialize models
def init_models(engine):
    Base.metadata.create_all(engine)


# Dependency injection
from sqlalchemy.orm import sessionmaker


def get_db(engine):
    Session = sessionmaker(bind=engine)
    db = Session()
    try:
        yield db
    finally:
        db.close()

from flask_login import UserMixin
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.db_config import Base


class AdminUser(Base, UserMixin):
    __tablename__ = "admin_users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=True)

    # Relationship
    business = relationship("Business", foreign_keys=[business_id])


class ChatbotLog(Base):
    __tablename__ = "chatbot_logs"
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"))
    user_message = Column(String)
    bot_response = Column(String)
    intent_detected = Column(String)
    timestamp = Column(String)  # ISO format timestamp

    # Relationship
    business = relationship("Business", foreign_keys=[business_id])
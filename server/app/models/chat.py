from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin, BaseModelMixin


class Conversation(Base, BaseModelMixin, TimestampMixin):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    title = Column(String(255), nullable=True)
    pinned = Column(String(5), default="false", nullable=False)

    user = relationship("User", back_populates="chat_conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    __table_args__ = (Index("ix_conversation_user", "user_id"),)


class Message(Base, BaseModelMixin, TimestampMixin):
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversation.id"), nullable=False)
    sender = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    message_type = Column(String(50), default="text", nullable=False)

    conversation = relationship("Conversation", back_populates="messages")
    __table_args__ = (Index("ix_message_conversation", "conversation_id"),)

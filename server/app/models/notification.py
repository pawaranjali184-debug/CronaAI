from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin, BaseModelMixin


class Notification(Base, BaseModelMixin, TimestampMixin):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=True)
    priority = Column(String(50), default="normal", nullable=False)
    read = Column(String(5), default="false", nullable=False)

    user = relationship("User", back_populates="notifications")
    __table_args__ = (Index("ix_notification_user", "user_id"),)

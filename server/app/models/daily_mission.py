from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin, BaseModelMixin


class DailyMission(Base, BaseModelMixin, TimestampMixin):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    mission_type = Column(String(100), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    scheduled_for = Column(DateTime, nullable=True)
    status = Column(String(50), default="pending", nullable=False)

    user = relationship("User", back_populates="tasks")
    history = relationship("MissionHistory", back_populates="mission", cascade="all, delete-orphan")
    __table_args__ = (Index("ix_daily_mission_user", "user_id"),)


class MissionHistory(Base, BaseModelMixin, TimestampMixin):
    id = Column(Integer, primary_key=True, index=True)
    mission_id = Column(Integer, ForeignKey("dailymission.id"), nullable=False)
    completed_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)

    mission = relationship("DailyMission", back_populates="history")

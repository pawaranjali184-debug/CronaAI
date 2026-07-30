from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin, BaseModelMixin


class Goal(Base, BaseModelMixin, TimestampMixin):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    target_date = Column(DateTime, nullable=True)
    status = Column(String(50), default="active", nullable=False)

    user = relationship("User", back_populates="goals")
    progress = relationship("GoalProgress", back_populates="goal", cascade="all, delete-orphan")
    __table_args__ = (Index("ix_goal_user", "user_id"),)


class GoalProgress(Base, BaseModelMixin, TimestampMixin):
    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey("goal.id"), nullable=False)
    completed_at = Column(DateTime, nullable=True)
    percentage = Column(Integer, default=0, nullable=False)
    note = Column(Text, nullable=True)

    goal = relationship("Goal", back_populates="progress")

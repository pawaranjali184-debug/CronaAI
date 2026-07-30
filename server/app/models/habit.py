from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin, BaseModelMixin


class Habit(Base, BaseModelMixin, TimestampMixin):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    name = Column(String(255), nullable=False)
    frequency = Column(String(100), nullable=True)
    target = Column(String(100), nullable=True)
    status = Column(String(50), default="active", nullable=False)

    user = relationship("User", back_populates="habits")
    logs = relationship("HabitLog", back_populates="habit", cascade="all, delete-orphan")
    __table_args__ = (Index("ix_habit_user", "user_id"),)


class HabitLog(Base, BaseModelMixin, TimestampMixin):
    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habit.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    status = Column(String(50), default="completed", nullable=False)
    notes = Column(String(255), nullable=True)

    habit = relationship("Habit", back_populates="logs")

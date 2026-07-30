from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin, BaseModelMixin


class CareerRoadmap(Base, BaseModelMixin, TimestampMixin):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    goal_title = Column(String(255), nullable=False)
    summary = Column(Text, nullable=False)
    timeline = Column(Text, nullable=True)
    resources = Column(Text, nullable=True)

    user = relationship("User", back_populates="career_roadmaps")
    milestones = relationship("CareerMilestone", back_populates="roadmap", cascade="all, delete-orphan")


class CareerMilestone(Base, BaseModelMixin, TimestampMixin):
    id = Column(Integer, primary_key=True, index=True)
    roadmap_id = Column(Integer, ForeignKey("careerroadmap.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(DateTime, nullable=True)
    completed = Column(String(5), default="false", nullable=False)

    roadmap = relationship("CareerRoadmap", back_populates="milestones")
    __table_args__ = (Index("ix_career_milestone_roadmap", "roadmap_id"),)

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin, BaseModelMixin


class Skill(Base, BaseModelMixin, TimestampMixin):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    user_skills = relationship("UserSkill", back_populates="skill", cascade="all, delete-orphan")


class UserSkill(Base, BaseModelMixin, TimestampMixin):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skill.id"), nullable=False)
    level = Column(String(50), nullable=False)
    confidence = Column(Float, default=0.0, nullable=False)

    skill = relationship("Skill", back_populates="user_skills")
    __table_args__ = (Index("ix_user_skill", "user_id", "skill_id"),)


class SkillGapReport(Base, BaseModelMixin, TimestampMixin):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    target_job = Column(String(255), nullable=False)
    missing_skills = Column(Text, nullable=False)
    priority_order = Column(Text, nullable=False)
    readiness_score = Column(Float, nullable=False)


class Course(Base, BaseModelMixin, TimestampMixin):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    provider = Column(String(150), nullable=True)
    url = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)


class LearningProgress(Base, BaseModelMixin, TimestampMixin):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
    progress = Column(Float, default=0.0, nullable=False)
    status = Column(String(50), default="not started", nullable=False)

    __table_args__ = (Index("ix_learning_progress", "user_id", "course_id"),)

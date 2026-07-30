from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, Index, Boolean
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.base import TimestampMixin, BaseModelMixin


class Badge(Base, BaseModelMixin, TimestampMixin):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    achievements = relationship(
        "Achievement",
        back_populates="badge"
    )


class Level(Base, BaseModelMixin, TimestampMixin):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    threshold = Column(Float, nullable=False)

    achievements = relationship(
        "Achievement",
        back_populates="level"
    )


class Achievement(Base, BaseModelMixin, TimestampMixin):
    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("user.id"),
        nullable=False
    )

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    points = Column(
        Float,
        default=0.0,
        nullable=False
    )

    badge_id = Column(
        Integer,
        ForeignKey("badge.id"),
        nullable=True
    )

    level_id = Column(
        Integer,
        ForeignKey("level.id"),
        nullable=True
    )

    completed = Column(
        Boolean,
        default=False,
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="achievements"
    )

    badge = relationship(
        "Badge",
        back_populates="achievements"
    )

    level = relationship(
        "Level",
        back_populates="achievements"
    )

    __table_args__ = (
        Index("ix_achievement_user", "user_id"),
    )
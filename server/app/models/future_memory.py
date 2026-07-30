from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin, BaseModelMixin


class MemoryCategory(Base, BaseModelMixin, TimestampMixin):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    memories = relationship("FutureMemory", back_populates="category")


class FutureMemory(Base, BaseModelMixin, TimestampMixin):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("memorycategory.id"), nullable=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(String(255), nullable=True)
    summary = Column(Text, nullable=True)
    # metadata column is reserved by SQLAlchemy Declarative API

    user = relationship("User", back_populates="memories")
    category = relationship("MemoryCategory", back_populates="memories")
    __table_args__ = (Index("ix_future_memory_user", "user_id"),)

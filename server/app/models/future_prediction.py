from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin, BaseModelMixin


class FuturePrediction(Base, BaseModelMixin, TimestampMixin):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    input_data = Column(Text, nullable=False)
    career_prediction = Column(Text, nullable=False)
    salary_estimate = Column(String(100), nullable=True)
    success_probability = Column(Float, nullable=True)
    recommendations = Column(Text, nullable=True)

    user = relationship("User", back_populates="predictions")
    __table_args__ = (Index("ix_future_prediction_user", "user_id"),)

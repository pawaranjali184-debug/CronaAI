from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
from app.models.base import TimestampMixin, BaseModelMixin


class RefreshToken(Base, BaseModelMixin, TimestampMixin):
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(255), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="refresh_tokens")
    __table_args__ = (Index("ix_refresh_token_token", "token"),)

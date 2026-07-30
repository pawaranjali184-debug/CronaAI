from datetime import datetime
from sqlalchemy import Column, DateTime, Boolean
from sqlalchemy.ext.declarative import declared_attr


class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)


class BaseModelMixin:
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base
from app.models.base import TimestampMixin, BaseModelMixin


class Setting(Base, BaseModelMixin, TimestampMixin):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    key = Column(String(100), nullable=False)
    value = Column(Text, nullable=True)

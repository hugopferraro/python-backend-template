from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func

from src.domain.vo.domain_id import DomainID


class BaseModel(DeclarativeBase):
    __abstract__ = True

    id: Mapped[DomainID] = mapped_column(String, primary_key=True, default=DomainID.generate())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

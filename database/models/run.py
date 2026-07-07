from sqlalchemy import Integer, String, DateTime, Numeric, func
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime
from decimal import Decimal

from typing import TYPE_CHECKING

from ..base import Base

if TYPE_CHECKING:
    from models import Coverpoint

class Run(Base):
    __tablename__ = "runs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    run_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    result: Mapped[str] = mapped_column(String, nullable=False)
    checks: Mapped[int] = mapped_column(Integer)
    overall_coverage: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    uploaded_by: Mapped[str | None] = mapped_column(String, nullable=True)
    coverpoints: Mapped[list["Coverpoint"]] = relationship(
        "Coverpoint",
        back_populates="run",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

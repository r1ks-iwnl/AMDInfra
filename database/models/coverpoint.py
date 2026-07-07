from sqlalchemy import Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from decimal import Decimal

from typing import TYPE_CHECKING

from ..base import Base

if TYPE_CHECKING:
    from models import Run, Bin

class Coverpoint(Base):
    __tablename__ = "coverpoints"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("runs.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String, nullable=False)
    coverage: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    run: Mapped["Run"] = relationship("Run", back_populates="coverpoints")
    bins: Mapped[list["Bin"]] = relationship(
        "Bin",
        back_populates="coverpoint",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

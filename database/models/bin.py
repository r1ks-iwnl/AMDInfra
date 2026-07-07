from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from typing import TYPE_CHECKING

from ..base import Base

if TYPE_CHECKING:
    from models import Coverpoint

class Bin(Base):
    __tablename__ = "bins"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    coverpoint_id: Mapped[int] = mapped_column(
        ForeignKey("coverpoints.id", ondelete="CASCADE")
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    value: Mapped[str | None] = mapped_column(String, nullable=True)
    hits: Mapped[int] = mapped_column(Integer, nullable=False)
    hit: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coverpoint: Mapped["Coverpoint"] = relationship(
        "Coverpoint", back_populates="bins"
    )
